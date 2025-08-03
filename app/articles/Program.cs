using articles.Services;
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();
builder.Services.AddHttpClient<IArticleService, ArticleService>();
var dsn = builder.Configuration["Sentry:Dsn"];
builder.WebHost.UseSentry(o =>
{
    o.Dsn = dsn;
    o.TracesSampleRate = 1.0;
    o.SendDefaultPii = true;
    o.SetBeforeSend((@event, hint) =>
    {
        @event.ServerName = null;
        return @event;
    });
});
var tunnelUrl = builder.Configuration["Sentry:TunnelUrl"];
builder.Services.Configure<SentryTunnelOptions>(o => o.Url = tunnelUrl);
builder.Services.AddSentryTunneling("sentry.io");
var app = builder.Build();
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseSentryTunneling("/tunnel");
app.UseRouting();
app.UseAuthorization();
app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Article}/{action=Index}/{id?}")
    .WithStaticAssets();


app.Run();
