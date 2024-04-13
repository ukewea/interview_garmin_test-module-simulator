using Microsoft.Extensions.Logging;
using TestModuleSimulator.TestModules;
using TestModuleSimulator.Writers;

namespace TestModuleSimulator.Checkers
{
    public class RecentResultChecker : Checker
    {
        public RecentResultChecker(Writer resultWriter, CancellationToken stopToken, ILogger logger)
            : base(resultWriter, stopToken, logger)
        {
        }

        public override void ReceiveResult(TestModule sender, string result)
        {
            if (StopToken.IsCancellationRequested)
            {
                Logger.LogWarning("received result while cancellation is requested");
                return;
            }

            if (!KnownTestModules.ContainsKey(sender))
            {
                throw new InvalidOperationException("received result from unknown sender");
            }

            Logger.LogInformation($"{DateTime.Now} --> Received Result: {result}; from {sender}");
            lock (ResultsLock)
            {
                AddTestResult(sender, result);
                if (IsResultCompleteAndIdentical())
                {
                    Logger.LogInformation("all test results are `{0}`, output to writer", result);
                    DateTime maxTime = Results.Values.Max(r => r.Item1);
                    ResultWriter.Write(maxTime, result);
                }
            }
        }
    }
}
