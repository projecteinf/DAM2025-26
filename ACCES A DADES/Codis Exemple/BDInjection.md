
// Nom fitxer: 14-BDInjection/ADO/Program.cs
```CSharp


﻿using Microsoft.Extensions.Configuration;
using dbdemo.Services;
using dbdemo.Endpoints;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Configuració
builder.Configuration
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

string connectionString = builder.Configuration.GetConnectionString("DefaultConnection")!;

builder.Services.AddScoped<IDatabaseConnection>(sp =>
    new DatabaseConnection(builder.Configuration.GetConnectionString("DefaultConnection")!)
);


WebApplication webApp = builder.Build();

webApp.MapProductEndpoints();

webApp.Run();





```


// Nom fitxer: 14-BDInjection/ADO/Repository/ProductADO.cs
```CSharp


using Microsoft.Data.SqlClient;
using static System.Console;
using dbdemo.Services;
using dbdemo.Model;

namespace dbdemo.Repository;

class ProductADO
{
   
    public static void Insert(IDatabaseConnection dbConn,Product product)    // El mètode ha de passar a ser static
    {

        dbConn.Open();

        string sql = @"INSERT INTO Products (Id, Code, Name, Price)
                        VALUES (@Id, @Code, @Name, @Price)";

        using SqlCommand cmd = new SqlCommand(sql, dbConn.GetConnection());
        cmd.Parameters.AddWithValue("@Id", product.Id);
        cmd.Parameters.AddWithValue("@Code", product.Code);
        cmd.Parameters.AddWithValue("@Name", product.Name);
        cmd.Parameters.AddWithValue("@Price", product.Price);

        int rows = cmd.ExecuteNonQuery();
        Console.WriteLine($"{rows} fila inserida.");
        dbConn.Close();
    }

    public static void Update(IDatabaseConnection dbConn, Product product)
    {
        dbConn.Open();

        string sql = @"UPDATE Products
                    SET Code = @Code,
                        Name = @Name,
                        Price = @Price,
                        Image = @Image
                    WHERE Id = @Id";

        using SqlCommand cmd = new SqlCommand(sql, dbConn.GetConnection());
        cmd.Parameters.AddWithValue("@Id", product.Id);
        cmd.Parameters.AddWithValue("@Code", product.Code);
        cmd.Parameters.AddWithValue("@Name", product.Name);
        cmd.Parameters.AddWithValue("@Price", product.Price);
        cmd.Parameters.AddWithValue("@Image", product.ImagePath);

        int rows = cmd.ExecuteNonQuery();

        Console.WriteLine($"{rows} fila actualitzada.");
        
        dbConn.Close();
    }

    public static List<Product> GetAll(IDatabaseConnection dbConn, int limit)
    {
        List<Product> products = new();

        dbConn.Open();
        string sql = $"SELECT TOP {limit} Id, Code, Name, Price FROM Products";

        using SqlCommand cmd = new SqlCommand(sql, dbConn.GetConnection());
        using SqlDataReader reader = cmd.ExecuteReader();

        while (reader.Read())
        {
            products.Add(new Product
            {
                Id = reader.GetGuid(0),
                Code = reader.GetString(1),
                Name = reader.GetString(2),
                Price = reader.GetDecimal(3)
            });
        }

        dbConn.Close();
        return products;
    }

    public static Product? GetById(IDatabaseConnection dbConn, Guid id)
    {
        dbConn.Open();
        string sql = "SELECT Id, Code, Name, Price FROM Products WHERE Id = @Id";

        using SqlCommand cmd = new SqlCommand(sql, dbConn.GetConnection());
        cmd.Parameters.AddWithValue("@Id", id);

        using SqlDataReader reader = cmd.ExecuteReader();
        Product? product = null;    // Si no inicialitzem la variable => no existeix en el return!

        if (reader.Read())
        {
            product = new Product
            {
                Id = reader.GetGuid(0),
                Code = reader.GetString(1),
                Name = reader.GetString(2),
                Price = reader.GetDecimal(3)
            };
        }

        dbConn.Close();
        return product;
    }

    public static bool Delete(IDatabaseConnection dbConn, Guid id)
    {
        dbConn.Open();

        string sql = @"DELETE FROM Products WHERE Id = @Id";

        using SqlCommand cmd = new SqlCommand(sql, dbConn.GetConnection());
        cmd.Parameters.AddWithValue("@Id", id);

        int rows = cmd.ExecuteNonQuery();

        dbConn.Close();

        return rows > 0; // True si s'ha eliminat almenys una fila
    }

}

```


// Nom fitxer: 14-BDInjection/ADO/EndPoints/Product.cs
```CSharp


using dbdemo.Repository;
using dbdemo.Services;
using dbdemo.Model;
using dbdemo.DTO;
using dbdemo.Validators;
using dbdemo.Common;

namespace dbdemo.Endpoints;

public static class EndpointsProducts
{
    public static void MapProductEndpoints(this WebApplication app)
    {
        // GET /products
        // http://localhost:5000/products?total=10
        app.MapGet("/products", (IDatabaseConnection dbConn,int? total) =>
        {
            int limit = total ?? 20; 
            Console.WriteLine($"TOTAL PRODUCTES {limit}");
            List<Product>  products = ProductADO.GetAll(dbConn,limit);
            List<ProductResponse> productsResponse = new List<ProductResponse>();
            foreach (Product product in products) 
            {
                productsResponse.Add(ProductResponse.FromProduct(product));
            }
            
            return Results.Ok(productsResponse);
        });

        // GET Product by id
        app.MapGet("/products/{id}", (Guid id, IDatabaseConnection dbConn) =>
        {
            Product? product = ProductADO.GetById(dbConn, id);
            
            return product is not null
                ? Results.Ok(ProductResponse.FromProduct(product))
                : Results.NotFound(new { message = $"Product with Id {id} not found." });
        });

        // POST /products
        app.MapPost("/products", (ProductRequest req, IDatabaseConnection dbConn) =>
        {
            Guid id;
            Result result = ProductValidator.Validate(req);
            if (!result.IsOk)
            {
                return Results.BadRequest(new 
                {
                    error = result.ErrorCode,
                    message = result.ErrorMessage
                });
            }

            id = Guid.NewGuid();
            Product product = req.ToProduct(id);
            ProductADO.Insert(dbConn, product);

            return Results.Created($"/products/{product.Id}", ProductResponse.FromProduct(product));
        });

        app.MapPut("/products/{id}", (Guid id, ProductRequest req, IDatabaseConnection dbConn) =>
        {
            Result result = ProductValidator.Validate(req);
            if (!result.IsOk)
            {
                return Results.BadRequest(new 
                {
                    error = result.ErrorCode,
                    message = result.ErrorMessage
                });
            }

            Product? product = ProductADO.GetById(dbConn, id);

            if (product == null)
            {
                return Results.NotFound();
            }

            Product productUpdt = req.ToProduct(product.Id);

            ProductADO.Update(dbConn, productUpdt);

            return Results.Ok(ProductResponse.FromProduct(productUpdt)); 
        });

        // DELETE /products/{id}
        app.MapDelete("/products/{id}", (Guid id, IDatabaseConnection dbConn) => ProductADO.Delete(dbConn, id) ? Results.NoContent() : Results.NotFound());

        // POST  /products/{id}/upload

        app.MapPost("/products/{id}/upload", async (Guid id, IFormFile image, IDatabaseConnection dbConn) =>
        {
            if (image == null || image.Length == 0)
                return Results.BadRequest(new { message = "No s'ha rebut cap imatge." });

            
            Product? product = ProductADO.GetById(dbConn, id);
            if (product is null)
                return Results.NotFound(new { message = $"Producte amb Id {id} no trobat." });

            string filePath = await SaveImage(id,image);            

            product.ImagePath = filePath;
            ProductADO.Update(dbConn, product);

            return Results.Ok(new { message = "Imatge pujada correctament.", path = filePath });
        }).DisableAntiforgery();
    }

    public static async Task<string> SaveImage(Guid id, IFormFile image)
    {
        string uploadsFolder = Path.Combine(Directory.GetCurrentDirectory(), "uploads");

        if (!Directory.Exists(uploadsFolder))
            Directory.CreateDirectory(uploadsFolder);

        string fileName = $"{id}_{Path.GetFileName(image.FileName)}";
        string filePath = Path.Combine(uploadsFolder, fileName);

        using (FileStream stream = new FileStream(filePath, FileMode.Create))
        {
            await image.CopyToAsync(stream);
        }

        return filePath;
    }
}




```


// Nom fitxer: 14-BDInjection/ADO/DTO/ProductResponse.cs
```CSharp


using dbdemo.Model;

namespace dbdemo.DTO;

public record ProductResponse(Guid Id, string Code, string Name, decimal Price) 
{
    // Guanyem CONTROL sobre com es fa la conversió

    public static ProductResponse FromProduct(Product product)   // Conversió de model a response
    {
        return new ProductResponse(product.Id, product.Code, product.Name, product.Price);
    }
}

```


// Nom fitxer: 14-BDInjection/ADO/DTO/ProductRequest.cs
```CSharp


/*
DTO (Data Transfer Object): És una representació simplificada de les dades que es volen transferir 
entre les capes. Sovint és una estructura més lleugera que una entitat del model de dades, amb només 
les propietats necessàries per ser transportades entre les capes. 

Per exemple, el ProductRequest és un DTO perquè encapsula només les propietats necessàries per crear o 
actualitzar un producte a través de la API, sense necessitar totes les propietats que podrien formar part 
del model de dades intern.
*/
using dbdemo.Model;

namespace dbdemo.DTO;

public record ProductRequest(string Code, string Name, decimal Price) 
{
    // Guanyem CONTROL sobre com es fa la conversió

    public Product ToProduct(Guid id)   // Conversió a model
    {
        return new Product
        {
            Id = id,
            Code = Code,
            Name = Name,
            Price = Price
        };
    }
}

```


// Nom fitxer: 14-BDInjection/ADO/Validators/ProductValidator.cs
```CSharp


using dbdemo.DTO;
using dbdemo.Common;

namespace dbdemo.Validators;

public static class ProductValidator
{
    public static Result Validate(ProductRequest product)
    {
        if (product.Price <= 0)
        {
            return Result.Failure("El preu ha de ser superior a 0","PREU_INCORRECTE");
        }
        return Result.Ok();
    }

}

```


// Nom fitxer: 14-BDInjection/ADO/Model/Product.cs
```CSharp


namespace dbdemo.Model;

public class Product
{
    public Guid Id { get; set; }
    public string Code { get; set; } = "";
    public string Name { get; set; } = "";
    public decimal Price { get; set; }
    public string ImagePath { get; set; } = "";
}



```


// Nom fitxer: 14-BDInjection/ADO/Services/DatabaseConnection.cs
```CSharp


using Microsoft.Data.SqlClient;
using static System.Console;
using dbdemo.Model;

namespace dbdemo.Services;

public class DatabaseConnection : IDatabaseConnection
{
    private readonly string _connectionString;
    public SqlConnection? sqlConnection;
    public DatabaseConnection(string connectionString)
    {
        _connectionString = connectionString;
    }
    public SqlConnection GetConnection()
    {
        return sqlConnection!;
    }


    public bool Open()
    {
        sqlConnection = new SqlConnection(_connectionString);

        try
        {
            sqlConnection.Open();
            return true;
        }
        catch (Exception ex)
        {
            return false;
        }
    }
    public void Close()
    {
        sqlConnection?.Close();
    }
}


```


// Nom fitxer: 14-BDInjection/ADO/Services/Interfaces/IDatabase.cs
```CSharp


using Microsoft.Data.SqlClient;

namespace dbdemo.Services;

public interface IDatabaseConnection {
    SqlConnection GetConnection();
    bool Open();
    void Close();
}

```


// Nom fitxer: 14-BDInjection/ADO/Common/Result.cs
```CSharp


namespace dbdemo.Common;

public class Result
{
    public bool IsOk { get; }
    public string? ErrorMessage { get; }
    public string? ErrorCode { get; }

    private Result(bool ok, string? message = null, string? code = null)
    {
        IsOk = ok;
        ErrorCode = code;
        ErrorMessage = message;
    }

    public static Result Ok() => new Result(true);
    public static Result Failure(string message, string? code) =>
        new Result(false, message, code); 
}

```


