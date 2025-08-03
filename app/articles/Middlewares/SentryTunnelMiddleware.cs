using Microsoft.Extensions.Options;
public class SentryTunnelMiddleware
{
    private readonly RequestDelegate _next;
    private readonly HttpClient _httpClient;
    private readonly string _sentryUrl;
    

    public SentryTunnelMiddleware(RequestDelegate next, IOptions<SentryTunnelOptions> options)
    {
        _sentryUrl = options.Value.Url ?? string.Empty;
        _next = next;
        _httpClient = new HttpClient();
    }

    public async Task InvokeAsync(HttpContext context)
    {
        Console.WriteLine("Request passed through SentryTunnelMiddleware 🙆🙆🙆 ");
        if (!HttpMethods.IsPost(context.Request.Method))
        {
            context.Response.StatusCode = StatusCodes.Status405MethodNotAllowed;
            return;
        }

        var requestBody = await new StreamReader(context.Request.Body).ReadToEndAsync();

        var sentryUrl = _sentryUrl;

        var request = new HttpRequestMessage(HttpMethod.Post, sentryUrl)
        {
            Content = new StringContent(requestBody, System.Text.Encoding.UTF8, context.Request.ContentType)
        };

        foreach (var header in context.Request.Headers)
        {
            if (header.Key.StartsWith("X-Sentry") || header.Key == "Origin")
            {
                request.Headers.TryAddWithoutValidation(header.Key, header.Value.ToString());
            }
        }

        try
        {
            var response = await _httpClient.SendAsync(request);
            context.Response.StatusCode = (int)response.StatusCode;
        }
        catch (Exception)
        {
            context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        }
    }
}