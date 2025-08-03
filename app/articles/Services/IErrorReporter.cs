public interface IErrorReporter
{
    Task CaptureAsync(Exception exception);
    Task CaptureAsync(string message);
}