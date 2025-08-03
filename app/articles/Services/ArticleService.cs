using System.Text.Json;
using articles.Models;

namespace articles.Services
{
    public class ArticleService : IArticleService
    {
        private readonly HttpClient _httpClient;

        public ArticleService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<Article>> GetArticlesAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync("<API-EXTERNAL>");
                response.EnsureSuccessStatusCode();

                var json = await response.Content.ReadAsStringAsync();
                if (string.IsNullOrEmpty(json))
                {
                    throw new Exception("Received empty JSON response.");
                }

                var articles = JsonSerializer.Deserialize<List<Article>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                if (articles == null)
                {
                    throw new Exception("Deserialization resulted in a null object.");
                }

                return articles;
            }
            catch (HttpRequestException e)
            {
                throw new Exception($"Request error 😬: {e.Message}", e);
            }
            catch (JsonException e)
            {
                throw new Exception($"Deserialization error: {e.Message}", e);
            }
            catch (Exception e)
            {
                throw new Exception($"An error occurred: {e.Message}", e);
            }
        }

       
    }
}
