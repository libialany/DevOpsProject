using articles.Models;

namespace articles.Services
{
    public interface IArticleService
    {
        Task<List<Article>> GetArticlesAsync();
    }
}
