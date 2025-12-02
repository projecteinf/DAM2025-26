
// Nom fitxer: 20-ServiceExtensions/ADO/Extensions/ProductServicesExtensions.cs
```CSharp


using dbdemo.Repository;

namespace dbdemo.Extensions;

public static class ProductServicesExtensions
{
    public static IServiceCollection AddProductServices(this IServiceCollection services)
    {
        services.AddScoped<IQueryBuilderProduct, QueryBuilderProductMSSQL>();
        services.AddScoped<IProductRepo, ProductMSSQL>();
        return services;
    }
}


```


// Nom fitxer: 20-ServiceExtensions/ADO/Repository/ProductPostgres.cs
```CSharp


using System.Data;
using dbdemo.Services;
using dbdemo.Model;

namespace dbdemo.Repository;

public class ProductPostgres : IProductRepo
{
    private readonly IDatabaseConnection _db;

    public ProductPostgres(IDatabaseConnection db)
    {
        _db = db;
    }
    public void Insert(Product product)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = $@"INSERT INTO products (Id, Code, Name, Price)
                            VALUES (@Id, @Code, @Name, @Price)";

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = product.Id;
        cmd.Parameters.Add(paramId);

        var paramCode = cmd.CreateParameter();
        paramCode.ParameterName = "@Code";
        paramCode.Value = product.Code;
        cmd.Parameters.Add(paramCode);

        var paramName = cmd.CreateParameter();
        paramName.ParameterName = "@Name";
        paramName.Value = product.Name;
        cmd.Parameters.Add(paramName);

        var paramPrice = cmd.CreateParameter();
        paramPrice.ParameterName = "@Price";
        paramPrice.Value = product.Price;
        cmd.Parameters.Add(paramPrice);

        int rows = cmd.ExecuteNonQuery();
        Console.WriteLine($"{rows} fila inserida.");       
    }

    public void Update(Product product)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = $@"UPDATE products
                            SET Code = @Code,
                                Name = @Name,
                                Price = @Price,
                                Image = @Image
                            WHERE Id = @Id";

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = product.Id;
        cmd.Parameters.Add(paramId);

        var paramCode = cmd.CreateParameter();
        paramCode.ParameterName = "@Code";
        paramCode.Value = product.Code;
        cmd.Parameters.Add(paramCode);

        var paramName = cmd.CreateParameter();
        paramName.ParameterName = "@Name";
        paramName.Value = product.Name;
        cmd.Parameters.Add(paramName);

        var paramPrice = cmd.CreateParameter();
        paramPrice.ParameterName = "@Price";
        paramPrice.Value = product.Price;
        cmd.Parameters.Add(paramPrice);

        var paramImage = cmd.CreateParameter();
        paramImage.ParameterName = "@Image";
        paramImage.Value = product.ImagePath ?? (object)DBNull.Value;
        cmd.Parameters.Add(paramImage);

        int rows = cmd.ExecuteNonQuery();
        Console.WriteLine($"{rows} fila actualitzada.");
    }

    public List<Product> GetAll(int limit)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();
        string sql = $"SELECT Id, Code, Name, Price FROM products LIMIT {limit}";
        
        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = sql;

        List<Product> products = new List<Product>();
        using IDataReader reader = cmd.ExecuteReader();
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

        return products;
    }

    public Product? GetById(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = $"SELECT Id, Code, Name, Price FROM products WHERE Id = @Id";

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        Product? product = null;
        using IDataReader reader = cmd.ExecuteReader();
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
        return product;
    }

    public bool Delete(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = $"DELETE FROM products WHERE Id = @Id";

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        int rows = cmd.ExecuteNonQuery();
        return rows > 0;
    }
}


```


// Nom fitxer: 20-ServiceExtensions/ADO/Repository/IProductRepo.cs
```CSharp


using dbdemo.Model;

namespace dbdemo.Repository;

public interface IProductRepo
{
    List<Product> GetAll(int limit);
    Product? GetById(Guid id);
    void Insert(Product product);
    void Update(Product product);
    bool Delete(Guid id);
}


```


// Nom fitxer: 20-ServiceExtensions/ADO/Repository/IQueryBuilderProduct.cs
```CSharp


using dbdemo.Model;

namespace dbdemo.Repository;

public interface IQueryBuilderProduct
{
    string SelectAll(int n);
    string Insert(Product product);
    string Update(Product product);
    string SelectById();
    string Delete();

}

```


// Nom fitxer: 20-ServiceExtensions/ADO/Repository/QueryBuilderProductMSSQL.cs
```CSharp


using dbdemo.Model;

namespace dbdemo.Repository;

public class QueryBuilderProductMSSQL : IQueryBuilderProduct
{
    public string SelectAll(int limit)
    {
        return $"SELECT TOP ({limit}) Id, Code, Name, Price FROM products";
    }
    public string Insert(Product product)
    {
        return @"INSERT INTO products (Id, Code, Name, Price)
                            VALUES (@Id, @Code, @Name, @Price)";
    }
    public string Update(Product product)
    {
        return @"UPDATE products
                            SET Code = @Code,
                                Name = @Name,
                                Price = @Price,
                                Image = @Image
                            WHERE Id = @Id";
    }
    public string SelectById()
    {
        return "SELECT Id, Code, Name, Price FROM products WHERE Id = @Id";
    }
    public string Delete()
    {
        return "DELETE FROM products WHERE Id = @Id";
    }

}

```


// Nom fitxer: 20-ServiceExtensions/ADO/Repository/ProductMSSQL.cs
```CSharp


using Microsoft.Data.SqlClient;
using static System.Console;
using dbdemo.Services;
using dbdemo.Model;
using System.Data;

namespace dbdemo.Repository;

class ProductMSSQL : IProductRepo
{
    private readonly IDatabaseConnection _db;
    private readonly IQueryBuilderProduct _query;

    public ProductMSSQL(IDatabaseConnection db, IQueryBuilderProduct queryBuilder)
    {
        _db = db;
        _query = queryBuilder;
    }
    public void Insert(Product product)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.Insert(product);

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = product.Id;
        cmd.Parameters.Add(paramId);

        var paramCode = cmd.CreateParameter();
        paramCode.ParameterName = "@Code";
        paramCode.Value = product.Code;
        cmd.Parameters.Add(paramCode);

        var paramName = cmd.CreateParameter();
        paramName.ParameterName = "@Name";
        paramName.Value = product.Name;
        cmd.Parameters.Add(paramName);

        var paramPrice = cmd.CreateParameter();
        paramPrice.ParameterName = "@Price";
        paramPrice.Value = product.Price;
        cmd.Parameters.Add(paramPrice);

        int rows = cmd.ExecuteNonQuery();
        Console.WriteLine($"{rows} fila inserida.");

        
    }

    public void Update(Product product)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.Update(product);

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = product.Id;
        cmd.Parameters.Add(paramId);

        var paramCode = cmd.CreateParameter();
        paramCode.ParameterName = "@Code";
        paramCode.Value = product.Code;
        cmd.Parameters.Add(paramCode);

        var paramName = cmd.CreateParameter();
        paramName.ParameterName = "@Name";
        paramName.Value = product.Name;
        cmd.Parameters.Add(paramName);

        var paramPrice = cmd.CreateParameter();
        paramPrice.ParameterName = "@Price";
        paramPrice.Value = product.Price;
        cmd.Parameters.Add(paramPrice);

        var paramImage = cmd.CreateParameter();
        paramImage.ParameterName = "@Image";
        paramImage.Value = product.ImagePath ?? (object)DBNull.Value;
        cmd.Parameters.Add(paramImage);

        int rows = cmd.ExecuteNonQuery();
        Console.WriteLine($"{rows} fila actualitzada.");
    }

    public List<Product> GetAll(int limit)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();
        
        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.SelectAll(limit);

        List<Product> products = new List<Product>();
        using IDataReader reader = cmd.ExecuteReader();
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

        return products;
    }

    public Product? GetById(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.SelectById();

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        Product? product = null;
        using IDataReader reader = cmd.ExecuteReader();
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

        return product;
    }

    public bool Delete(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.Delete();

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        int rows = cmd.ExecuteNonQuery();
        return rows > 0;
    }
}


```


// Nom fitxer: 20-ServiceExtensions/ADO/Model/Product.cs
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


// Nom fitxer: 20-ServiceExtensions/ADO/DTO/ProductRequest.cs
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


// Nom fitxer: 20-ServiceExtensions/ADO/DTO/ProductResponse.cs
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


// Nom fitxer: 20-ServiceExtensions/ADO/Program.cs
```CSharp


﻿using Microsoft.Extensions.Configuration;
using dbdemo.Services;
using dbdemo.Endpoints;
using dbdemo.Repository;
using dbdemo.Extensions;


WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Configuració
builder.Configuration
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

builder.Services.AddProductServices();


builder.Services.AddScoped<IDatabaseConnection>(sp =>
    new DatabaseConnection(
        builder.Configuration.GetConnectionString("DefaultConnection")!
    )
);

// builder.Services.AddScoped<IProductRepo, ProductMSSQL>();
// builder.Services.AddScoped<IQueryBuilderProduct, QueryBuilderProductMSSQL>();

WebApplication webApp = builder.Build();

webApp.MapProductEndpoints();

webApp.Run();


/*
CREACIÓ CONTENIDOR DOCKER PER POSTGRESQL

docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  --restart=no \
  postgres:latest

docker start postgres

CREATE SCHEMA IF NOT EXISTS dbdemo;

-- Crear taula
CREATE TABLE dbdemo.products (
    id UUID NOT NULL,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    image VARCHAR(255),
    CONSTRAINT pk_products PRIMARY KEY (id)
);

*/



```


// Nom fitxer: 20-ServiceExtensions/ADO/EndPoints/Product.cs
```CSharp


using dbdemo.Repository;
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
        app.MapGet("/products", (IProductRepo productADO,int? total) =>
        {
            int limit = total ?? 20; 
            Console.WriteLine($"TOTAL PRODUCTES {limit}");
            List<Product>  products = productADO.GetAll(limit);
            List<ProductResponse> productsResponse = new List<ProductResponse>();
            foreach (Product product in products) 
            {
                productsResponse.Add(ProductResponse.FromProduct(product));
            }
            
            return Results.Ok(productsResponse);
        });

        // GET Product by id
        app.MapGet("/products/{id}", (Guid id, IProductRepo productADO) =>
        {
            Product? product = productADO.GetById(id);
            
            return product is not null
                ? Results.Ok(ProductResponse.FromProduct(product))
                : Results.NotFound(new { message = $"Product with Id {id} not found." });
        });

        // POST /products
        app.MapPost("/products", (ProductRequest req, IProductRepo productADO) =>
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
            productADO.Insert(product);

            return Results.Created($"/products/{product.Id}", ProductResponse.FromProduct(product));
        });

        app.MapPut("/products/{id}", (Guid id, ProductRequest req, IProductRepo productADO) =>
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

            Product? product = productADO.GetById(id);

            if (product == null)
            {
                return Results.NotFound();
            }

            Product productUpdt = req.ToProduct(product.Id);

            productADO.Update(productUpdt);

            return Results.Ok(ProductResponse.FromProduct(productUpdt)); 
        });

        // DELETE /products/{id}
        app.MapDelete("/products/{id}", (Guid id, IProductRepo productADO) => productADO.Delete(id) ? Results.NoContent() : Results.NotFound());

        // POST  /products/{id}/upload

        app.MapPost("/products/{id}/upload", async (Guid id, IFormFile image, IProductRepo productADO) =>
        {
            if (image == null || image.Length == 0)
                return Results.BadRequest(new { message = "No s'ha rebut cap imatge." });

            
            Product? product = productADO.GetById(id);
            if (product is null)
                return Results.NotFound(new { message = $"Producte amb Id {id} no trobat." });

            string filePath = await SaveImage(id,image);            

            product.ImagePath = filePath;
            productADO.Update(product);

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


// Nom fitxer: 20-ServiceExtensions/ADO/Common/Result.cs
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


// Nom fitxer: 20-ServiceExtensions/ADO/Services/DatabaseConnection.cs
```CSharp


using System.Data;
using Microsoft.Data.SqlClient;

namespace dbdemo.Services;

public class DatabaseConnection : IDatabaseConnection
{
    private readonly string _connectionString;

    public DatabaseConnection(string connectionString)
    {
        _connectionString = connectionString;
    }

    // Retorna una nova connexió SQL Server cada cop
    public IDbConnection GetConnection()
    {
        return new SqlConnection(_connectionString);
    }
    
}



```


// Nom fitxer: 20-ServiceExtensions/ADO/Services/PostgresConnection.cs
```CSharp


using System.Data;
using Npgsql;

namespace dbdemo.Services;

public class PostgresConnection : IDatabaseConnection
{
    private readonly string _connectionString;
    
    public PostgresConnection(string connectionString)
    {
        _connectionString = connectionString;
    }

    // Retorna una nova connexió Npgsql cada cop
    public IDbConnection GetConnection()
    {
        return new NpgsqlConnection(_connectionString);
    }
}



```


// Nom fitxer: 20-ServiceExtensions/ADO/Services/Interfaces/IDatabase.cs
```CSharp


using System.Data;


namespace dbdemo.Services;

public interface IDatabaseConnection {
    IDbConnection GetConnection();

}

```


// Nom fitxer: 20-ServiceExtensions/ADO/Validators/ProductValidator.cs
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


