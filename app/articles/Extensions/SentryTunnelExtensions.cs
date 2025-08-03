// using articles.Middlewares.SentryTunnelMiddleware;
public static class SentryTunnelExtensions
{
    public static void UseSentryTunneling(this IApplicationBuilder builder, string path = "/tunnel")
    {
        Console.WriteLine("SentryTunnelExtensions...🙆");
        builder.Map(path, app =>
        {
            app.UseMiddleware<SentryTunnelMiddleware>();
        });
    }
}