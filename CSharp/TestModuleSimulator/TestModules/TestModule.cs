using Microsoft.Extensions.Logging;

namespace TestModuleSimulator.TestModules
{
    public abstract class TestModule
    {
        protected readonly Func<TestModule, string, bool> Judge;
        protected readonly Action<TestModule, string> ReceiveResult;
        protected readonly CancellationToken StopToken;
        protected readonly ILogger Logger;

        private readonly Guid _id = Guid.NewGuid();

        protected TestModule(Func<TestModule, string, bool> judge,
            Action<TestModule, string> receiveResult, CancellationToken stopToken, ILogger logger)
        {
            Judge = judge;
            ReceiveResult = receiveResult;
            StopToken = stopToken;
            Logger = logger;
        }

        public Guid Id => _id;

        public abstract Task StartTestingAsync();
    }
}
