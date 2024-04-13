using Microsoft.Extensions.Logging;

namespace TestModuleSimulator.TestModules
{
    public class ManualTestModule : TestModule
    {
        private static readonly Random _random = new();

        public ManualTestModule(Func<TestModule, string, bool> judge,
            Action<TestModule, string> receiveResult, CancellationToken stopToken, ILogger logger)
            : base(judge, receiveResult, stopToken, logger)
        {
        }

        public override async Task StartTestingAsync()
        {
            while (!StopToken.IsCancellationRequested)
            {
                await Task.Delay(TimeSpan.FromSeconds(_random.Next(3, 11)));
                var result = Judge(this, string.Empty) ? "Pass" : "Fail";
                ReceiveResult(this, result);
            }
        }

        public override string ToString()
        {
            return $"{GetType().Name}";
        }
    }
}
