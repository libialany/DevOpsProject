using Microsoft.AspNetCore.Mvc;
using articles.Services;

namespace articles.Controllers
{
    public class ArticleController : Controller
    {
        private readonly IHub _sentryHub;

        private readonly IArticleService _articleService;

        public ArticleController(IArticleService articleService, IHub sentryHub)
        {
            _articleService = articleService;
            _sentryHub = sentryHub;
        }

        public async Task<IActionResult> Index()
        {
            var childSpan = _sentryHub.GetSpan()?.StartChild("additional-work");
            try
            {
                var articles = await _articleService.GetArticlesAsync();
                childSpan?.Finish(SpanStatus.Ok);
                return View(articles);
            }
            catch (System.Exception)
            {
                childSpan?.Finish(SpanStatus.InternalError);
                throw;
            }
        }
    }
}
