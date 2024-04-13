using FluentAssertions;
using NSubstitute;
using TestModuleSimulator.Checkers;
using TestModuleSimulator.TestModules;
using TestModuleSimulator.Writers;

#pragma warning disable CS8974

namespace TestModuleSimulator.UnitTests
{
    public class RecentResultCheckerTests
    {
        private readonly CancellationTokenSource cts = new();
        private readonly Writer resultWriter = GivenMockWriter();

        [Fact]
        public void ReceiveResult_UnknownModule_ThrowsException()
        {
            RecentResultChecker checker = GivenChecker(resultWriter);
            TestModule module1 = GivenRegisteredMockTestModule(checker);
            TestModule module2 = GivenMockTestModule(checker, registerToChecker: false);

            checker.Invoking(x => x.ReceiveResult(module2, "Pass"))
                .Should().Throw<InvalidOperationException>(
                    "Receive result from unknown module should raise exception");
        }

        [Fact]
        public void IsResultCompleteAndIdentical_IncompleteData_ReturnsFalse()
        {
            // Arrange
            RecentResultChecker checker = GivenChecker(resultWriter);
            TestModule module1 = GivenRegisteredMockTestModule(checker);
            TestModule _ = GivenRegisteredMockTestModule(checker);

            // Act
            checker.ReceiveResult(module1, "Pass");

            // Assert
            checker.IsResultCompleteAndIdentical().Should().BeFalse(
                "no test result sent from another yet");
            resultWriter.Received(0).Write(Arg.Any<DateTime>(), Arg.Any<string>());
        }

        [Fact]
        public void IsResultCompleteAndIdentical_CompleteButDiffResult_ReturnsFalse()
        {
            // Arrange
            RecentResultChecker checker = GivenChecker(resultWriter);
            TestModule module1 = GivenRegisteredMockTestModule(checker);
            TestModule module2 = GivenRegisteredMockTestModule(checker);

            // Act
            checker.ReceiveResult(module1, "Pass");
            checker.ReceiveResult(module2, "Fail");

            // Assert
            checker.IsResultCompleteAndIdentical().Should().BeFalse(
                "test results are not the same");
            resultWriter.Received(0).Write(Arg.Any<DateTime>(), Arg.Any<string>());
        }

        [Fact]
        public void IsResultCompleteAndIdentical_CompleteSameResult_ReturnsTrue()
        {
            // Arrange
            RecentResultChecker checker = GivenChecker(resultWriter);
            TestModule module1 = GivenRegisteredMockTestModule(checker);
            TestModule module2 = GivenRegisteredMockTestModule(checker);

            // Act
            checker.ReceiveResult(module1, "Pass");
            checker.ReceiveResult(module2, "Pass");

            // Assert
            checker.IsResultCompleteAndIdentical().Should().BeTrue(
                "all modules sent result and results are identical");
            resultWriter.Received(1).Write(Arg.Any<DateTime>(), Arg.Any<string>());
        }

        private static bool JudgePassOrFail(TestModule sender, string data)
        {
            // result is irrelevant
            return true;
        }

        private static Writer GivenMockWriter()
        {
            return Substitute.For<Writer>();
        }

        private RecentResultChecker GivenChecker(Writer resultWriter)
        {
            return new RecentResultChecker(resultWriter, cts.Token);
        }

        private TestModule GivenRegisteredMockTestModule(RecentResultChecker checker)
        {
            return GivenMockTestModule(checker, registerToChecker: true);
        }

        private TestModule GivenMockTestModule(RecentResultChecker checker,
          bool registerToChecker)
        {
            var m = Substitute.For<TestModule>(JudgePassOrFail, checker.ReceiveResult, cts.Token);
            if (registerToChecker)
                checker.RegisterTestModule(m);
            return m;
        }
    }
}
