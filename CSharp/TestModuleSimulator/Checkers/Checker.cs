using Microsoft.Extensions.Logging;
using System.Collections.Concurrent;
using TestModuleSimulator.TestModules;
using TestModuleSimulator.Writers;

namespace TestModuleSimulator.Checkers
{
    public abstract class Checker
    {
        protected readonly Writer ResultWriter;
        protected readonly object ResultsLock = new();
        protected readonly ConcurrentDictionary<Guid, Tuple<DateTime, object>> Results;
        protected readonly ConcurrentDictionary<TestModule, byte> KnownTestModules = new();
        protected readonly CancellationToken StopToken;
        protected readonly ILogger Logger;
        public Checker(Writer resultWriter, CancellationToken stopToken, ILogger logger)
        {
            ResultWriter = resultWriter;
            StopToken = stopToken;
            Results = new();
            Logger = logger;
        }

        public void RegisterTestModule(TestModule testModule)
        {
            KnownTestModules[testModule] = 0;
        }

        public void UnregisterTestModule(TestModule testModule)
        {
            KnownTestModules.TryRemove(testModule, out var _);
        }

        public void AddTestResult(TestModule sender, object result)
        {
            DateTime currentTime = DateTime.UtcNow;
            lock (ResultsLock)
            {
                Results[sender.Id] = new Tuple<DateTime, object>(currentTime, result);
            }
        }

        public bool IsResultCompleteAndIdentical()
        {
            lock (ResultsLock)
            {
                return Results.Count == KnownTestModules.Count && (
                    AllResultsAre("Pass") || AllResultsAre("Fail")
                );
            }
        }

        private bool AllResultsAre(string result)
        {
            foreach (var res in Results.Values)
            {
                if ((string)res.Item2 != result)
                {
                    return false;
                }
            }
            return true;
        }

        public virtual void StartBackgroundTask()
        {
        }

        public virtual void StopBackgroundTask()
        {
        }

        public abstract void ReceiveResult(TestModule sender, string result);
    }
}

