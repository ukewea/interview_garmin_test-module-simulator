using Microsoft.Extensions.Logging;
using TestModuleSimulator.Checkers;
using TestModuleSimulator.TestModules;
using TestModuleSimulator.Writers;

namespace TestModuleSimulator
{
    public class Program
    {
        private static readonly CancellationTokenSource _cts = new();
        private static readonly List<TestModule> _testModules = new();
        private static readonly Checker _checker;
        private static readonly ExcelWriter _resultWriter = new("./test_result.xlsx");
        private static readonly ILogger _logger;

        static Program()
        {
            using var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.AddConsole();
            });

            _logger = loggerFactory.CreateLogger<Program>();

            _checker = new RecentResultChecker(_resultWriter, _cts.Token, _logger);

            Console.CancelKeyPress += (sender, e) =>
            {
                _logger.LogInformation("Exiting...");
                e.Cancel = true;
                DoCleanUp();
            };
        }

        static void Main(string[] _)
        {
            _logger.LogInformation("Starting...");

            _testModules.Add(new AutoTestModule(JudgePassFail, _checker.ReceiveResult, _cts.Token, _logger, TimeSpan.FromSeconds(0.5)));
            _testModules.Add(new AutoTestModule(JudgePassFail, _checker.ReceiveResult, _cts.Token, _logger, TimeSpan.FromSeconds(1.8)));
            _testModules.Add(new ManualTestModule(JudgePassFail, _checker.ReceiveResult, _cts.Token, _logger));

            try
            {
                foreach (var m in _testModules)
                {
                    _checker.RegisterTestModule(m);
                }

                _checker.StartBackgroundTask();

                var tasks = new List<Task>();
                foreach (var m in _testModules)
                {
                    tasks.Add(Task.Run(() => m.StartTestingAsync()));
                }

                Task.WaitAll(tasks.ToArray());
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("Exiting...");
                DoCleanUp();
            }

            _logger.LogInformation("Exited");
        }

        private static bool JudgePassFail(TestModule sender, string rawData)
        {
            return new Random().Next(2) == 0;
        }

        private static void DoCleanUp()
        {
            _cts.Cancel();

            _checker.StopBackgroundTask();

            foreach (var m in _testModules)
            {
                _checker.UnregisterTestModule(m);
            }
        }
    }
}