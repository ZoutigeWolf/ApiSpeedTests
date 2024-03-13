namespace cs;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        
        builder.WebHost.UseUrls("http://localhost:8080");

        var app = builder.Build();

        app.MapGet("/", (HttpContext _) => "Hello world!");

        app.Run();
    }
}