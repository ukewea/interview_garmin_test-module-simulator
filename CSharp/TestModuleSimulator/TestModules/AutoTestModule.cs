using Microsoft.Extensions.Logging;

namespace TestModuleSimulator.TestModules
{
    public class AutoTestModule : TestModule
    {
        private readonly TimeSpan _testInterval;

        public AutoTestModule(Func<TestModule, string, bool> judge,
            Action<TestModule, string> receiveResult, CancellationToken stopToken,
            ILogger logger, TimeSpan testInterval)
            : base(judge, receiveResult, stopToken, logger)
        {
            _testInterval = testInterval;
        }

        public override async Task StartTestingAsync()
        {
            while (!StopToken.IsCancellationRequested)
            {
                await Task.Delay(_testInterval);
                var result = Judge(this, string.Empty) ? "Pass" : "Fail";
                ReceiveResult(this, result);
            }
        }

        public override string ToString()
        {
            return $"{GetType().Name} with {_testInterval.TotalSeconds}s interval";
        }
    }
}
