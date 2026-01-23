
// Nom fitxer: 23-CleanCodeLight/ADO/Domain/Entitites/Product.cs
```CSharp


namespace dbdemo.Domain.Entities;

public class Product
{
/*
ATENCIÓ
     En el domain no ha de constar Id ja que és una decisió de base de dades.
     Utilitzem Guid per què el nostre SGBD disposa d'aquest tipus de dades.
     L'entitat de domini de Product no ha de tenir aquest camp.
     El camp Id pertany exclusivament a l'entitat d'infraestructura (COM guardem el producte a la base de dades).
*/
    public Guid Id { get; set; }

    public string Code { get; set; } = "";
    public string Name { get; set; } = "";
    public decimal Price { get; set; }

    public Product(Guid id, string code, string name, decimal price)
    {
        Id=id;
        Code=code;
        Name=name;
        Price=price;
    }

}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Domain/Validators/ProductValidator.cs
```CSharp


using dbdemo.Domain.Entities;
using dbdemo.Common;


namespace dbdemo.Validators;

public static class ProductValidator
{
    public static Result Validate(Product product)
    {
        if (product.Price <= 0)
        {
            return Result.Failure("El preu ha de ser superior a 0","PREU_INCORRECTE");
        }
        return Result.Ok();
    }

}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Program.cs
```CSharp


﻿using Microsoft.Extensions.Configuration;
using dbdemo.Services;
using dbdemo.Endpoints;
using dbdemo.Repository;
using dbdemo.Extensions;
using Microsoft.OpenApi;

/*

    dotnet add package Swashbuckle.AspNetCore

*/

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Configuració
builder.Configuration
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

builder.Services.AddDatabase(builder.Configuration);
builder.Services.AddProductServices(builder.Configuration);

// builder.Services.AddScoped<IDatabaseConnection>(sp =>
//     new DatabaseConnection(
//         builder.Configuration.GetConnectionString("DefaultConnection")!
//     )
// );

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

WebApplication webApp = builder.Build();

webApp.UseRouting();

webApp.UseSwagger();
webApp.UseSwaggerUI();

/*
Si el volem utilitzar només per desenvolupament

if (webApp.Environment.IsDevelopment())
{
    webApp.UseSwagger();
    webApp.UseSwaggerUI();
}
*/

Console.WriteLine($"Environment: {webApp.Environment.EnvironmentName}");

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


// Nom fitxer: 23-CleanCodeLight/ADO/API/EndPoints/Product.cs
```CSharp


using dbdemo.Repository;
using dbdemo.DTO;
using dbdemo.Validators;
using dbdemo.Common;
using dbdemo.Domain.Entities;
using dbdemo.Infraestructure.Persistence.Entitites;
using dbdemo.Infraestructure.Mappers;

namespace dbdemo.Endpoints;

/*                                WORKFLOW


**************************     POST / PUT    **************************

                           Request DTO
                              ↓
                           Product (Domain)
                              ↓ validate
                           UseCase (NO Aplicat encara: la lògica de cas d’ús està dins l’endpoint)
                              ↓
                           Mapper
                              ↓
                           ProductEntity
                              ↓
                           ADO / SQL

**************************     GET     **************************

                           SQL / ADO
                              ↓
                           ProductEntity
                              ↓
                           Mapper
                              ↓
                           Product (Domain)
                              ↓
                           DTO Response

*/


/*                                CLASSES

Classe	                                                                Representa
dbdemo.Domain.Entities.Product              	            (Domain) Característiques producte del negoci (domini)
dbdemo.Validators.ProductValidator                          (Domain) Validació dades del negoci (no relacionades amb BD): ex. preu>0
dbdemo.Infraestructure.Persistence.Entitites.ProductEntity	(Camps taula BD) El registre de la base de dades (infraestructura). 
dbdemo.DTO.ProductRequest                                   (Body API) DTO d'entrada -> Informació que ens arriba de l'API (POST/PUT/PATCH)  (infraestructura)
dbdemo.DTO.ProductResponse                                  (Resposta API) Informació que retornem de l'API  (infraestructura)
dbdemo.Infraestructure.Mappers.ProductMapper                => Evita l’acoblament directe entre domini i persistència
                                                            (ToDomain) Conversió (mapeig) entitat base de dades a entitat de domini  (infraestructura)
                                                            (ToEntity) Conversió (mapeig) d'entitat de domini a entitat de base de dades (infraestructura)
dbdemo.Repository.ProductMSSQL                              (ADO / SQL) Operacions amb la base de dades (insert, select,...)

*/

/*
| Responsabilitat        | On està                 |
| ---------------------- | ----------------------- |
| Regles de negoci pures | Domain                  |
| Entrada / sortida HTTP | DTO                     |
| Persistència           | Repository              |
| Transformacions        | Mapper                  |
| Orquestració           | Endpoint (temporalment) |
*/



public static class EndpointsProducts
{
    public static void MapProductEndpoints(this WebApplication app)
    {
        // GET /products: http://localhost:5000/products?total=10
        
        app.MapGet("/products", (IProductRepo productADO,int? total) =>
        {
            int limit = total ?? 20; 
            
            List<ProductEntity>  products = productADO.GetAll(limit);
            List<ProductResponse> productsResponse = new List<ProductResponse>();
            foreach (ProductEntity productEntity in products) 
            {
                Product product = ProductMapper.ToDomain(productEntity);
                productsResponse.Add(ProductResponse.FromProduct(product));
            }
            
            return Results.Ok(productsResponse);
        }).WithTags("Products");

        // GET Product by id
        app.MapGet("/products/{id}", (Guid id, IProductRepo productADO) =>
        {
            ProductEntity? productEntity = (ProductEntity) productADO.GetById(id)!;
            Product product = ProductMapper.ToDomain(productEntity);
            return productEntity is not null
                ? Results.Ok(ProductResponse.FromProduct(product))
                : Results.NotFound(new { message = $"Product with Id {id} not found." });
        }).WithTags("Products");

        // POST /products
        app.MapPost("/products", (ProductRequest req, IProductRepo productADO) =>
        {
            Guid id;

            id = Guid.NewGuid();
            Product product = req.ToProduct(id);
            Result result = ProductValidator.Validate(product);
            if (!result.IsOk)
            {
                return Results.BadRequest(new 
                {
                    error = result.ErrorCode,
                    message = result.ErrorMessage
                });
            }
            ProductEntity productEntity = ProductMapper.ToEntity(product);
            productADO.Insert(productEntity);

            return Results.Created($"/products/{product.Id}", ProductResponse.FromProduct(product,productEntity.ImagePath));
        }).WithTags("Products");

        app.MapPut("/products/{id}", (Guid id, ProductRequest req, IProductRepo productADO) =>
        {
            if (productADO.GetById(id) == null)
            {
                return Results.NotFound();
            }
            
            Product product = req.ToProduct(id);    // Domain
            Result result = ProductValidator.Validate(product);
            
            if (!result.IsOk)
            {
                return Results.BadRequest(new 
                {
                    error = result.ErrorCode,
                    message = result.ErrorMessage
                });
            }

            ProductEntity productUpdt = ProductMapper.ToEntity(product);
            productADO.Update(productUpdt);

            return Results.Ok(ProductResponse.FromProduct(product)); 
        }).WithTags("Products");

        // DELETE /products/{id}
        app.MapDelete("/products/{id}", (Guid id, IProductRepo productADO) => productADO.Delete(id) ? Results.NoContent() : Results.NotFound()).WithTags("Products");

        // POST  /products/{id}/upload

        app.MapPost("/products/{id}/upload", async (Guid id, IFormFile image, IProductRepo productADO) =>
        {
            if (image == null || image.Length == 0)
                return Results.BadRequest(new { message = "No s'ha rebut cap imatge." });

            
            ProductEntity? product = (ProductEntity)productADO.GetById(id)!;
            if (product is null)
                return Results.NotFound(new { message = $"Producte amb Id {id} no trobat." });

            string filePath = await SaveImage(id,image);            

            product.ImagePath = filePath;
            productADO.Update(product);

            return Results.Ok(new { message = "Imatge pujada correctament.", path = filePath });
        }).WithTags("Products").DisableAntiforgery();
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


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Mappers/ProductManager.cs
```CSharp


using dbdemo.Infraestructure.Persistence.Entitites;
using dbdemo.Domain.Entities;

namespace dbdemo.Infraestructure.Mappers;

public static class ProductMapper
{
    public static Product ToDomain(ProductEntity entity)
        => new Product(
            entity.Id,
            entity.Code,
            entity.Name,
            entity.Price
        );

    public static ProductEntity ToEntity(Product product, string? imagePath = null)
        => new ProductEntity
        {
            Id = product.Id,
            Code = product.Code,
            Name = product.Name,
            Price = product.Price,
            ImagePath = imagePath
        };
}


```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/DTO/ProductResponse.cs
```CSharp


using dbdemo.Domain.Entities;

namespace dbdemo.DTO;

public record ProductResponse(Guid Id, string Code, string Name, decimal Price, string? ImagePath) 
{
    // Guanyem CONTROL sobre com es fa la conversió

    public static ProductResponse FromProduct(Product product,string? pathImage=null)   // Conversió d'entitat a response
    {
        return new ProductResponse(product.Id, product.Code, product.Name, product.Price, pathImage);
    }
}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/DTO/ProductRequest.cs
```CSharp


/*
DTO (Data Transfer Object): És una representació simplificada de les dades que es volen transferir 
entre les capes. Sovint és una estructura més lleugera que una entitat del model de dades, amb només 
les propietats necessàries per ser transportades entre les capes. 

Per exemple, el ProductRequest és un DTO perquè encapsula només les propietats necessàries per crear o 
actualitzar un producte a través de la API, sense necessitar totes les propietats que podrien formar part 
del model de dades intern.
*/

using dbdemo.Domain.Entities;

namespace dbdemo.DTO;

public record ProductRequest(string Code, string Name, decimal Price) 
{
    // Guanyem CONTROL sobre com es fa la conversió

    public Product ToProduct(Guid id)   // Conversió a model
    {
        return new Product(id,Code,Name,Price);
    }
}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Entitites/ProductEntity.cs
```CSharp


namespace dbdemo.Infraestructure.Persistence.Entitites;

public class ProductEntity 
{
    public Guid Id { get; set; }
    public required string Code { get; set; }
    public required string Name { get; set; }
    public required decimal Price { get; set; }
    public string? ImagePath { get; set; }

}



```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Repositories/ProductMSSQL.cs
```CSharp


using static System.Console;
using dbdemo.Services;
using System.Data;
using dbdemo.Infraestructure.Persistence.Entitites;

namespace dbdemo.Repository;

class ProductMSSQL  : IProductRepo
{
    private readonly IDatabaseConnection _db;
    private readonly IQueryBuilderProduct _query;

    public ProductMSSQL(IDatabaseConnection db, IQueryBuilderProduct queryBuilder)
    {
        _db = db;
        _query = queryBuilder;
    }
    public void Insert(ProductEntity product)
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

    public void Update(ProductEntity product)
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

    public List<ProductEntity> GetAll(int limit)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();
        
        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.SelectAll(limit);

        List<ProductEntity> products = new List<ProductEntity>();
        using IDataReader reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            products.Add(new ProductEntity
            {
                Id = reader.GetGuid(0),
                Code = reader.GetString(1),
                Name = reader.GetString(2),
                Price = reader.GetDecimal(3)
            });
        }

        return products;
    }

    public ProductEntity? GetById(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = _query.SelectById();

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        ProductEntity? product = null;
        using IDataReader reader = cmd.ExecuteReader();
        if (reader.Read())
        {
            product = new ProductEntity
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


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Repositories/Product/Interface/IQueryBuilderProduct.cs
```CSharp


using dbdemo.Infraestructure.Persistence.Entitites;

namespace dbdemo.Repository;

public interface IQueryBuilderProduct
{
    string SelectAll(int n);
    string Insert(ProductEntity product);
    string Update(ProductEntity product);
    string SelectById();
    string Delete();

}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Repositories/Product/Interface/IProductRepo.cs
```CSharp


using dbdemo.Infraestructure.Persistence.Entitites;

namespace dbdemo.Repository;

public interface IProductRepo
{
    List<ProductEntity> GetAll(int limit);
    ProductEntity? GetById(Guid id);
    void Insert(ProductEntity product);
    void Update(ProductEntity product);
    bool Delete(Guid id);
}


```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Repositories/Product/Postgres/ProductPostgres.cs
```CSharp


using System.Data;
using dbdemo.Services;
using dbdemo.Infraestructure.Persistence.Entitites;

namespace dbdemo.Repository;

public class ProductPostgres : IProductRepo
{
    private readonly IDatabaseConnection _db;

    public ProductPostgres(IDatabaseConnection db)
    {
        _db = db;
    }
    public void Insert(ProductEntity product)
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

    public void Update(ProductEntity product)
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

    public List<ProductEntity> GetAll(int limit)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();
        string sql = $"SELECT Id, Code, Name, Price FROM products LIMIT {limit}";
        
        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = sql;

        List<ProductEntity> products = new List<ProductEntity>();
        using IDataReader reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            products.Add(new ProductEntity
            {
                Id = reader.GetGuid(0),
                Code = reader.GetString(1),
                Name = reader.GetString(2),
                Price = reader.GetDecimal(3)
            });
        }

        return products;
    }

    public ProductEntity? GetById(Guid id)
    {
        using IDbConnection conn = _db.GetConnection();
        conn.Open();

        using IDbCommand cmd = conn.CreateCommand();
        cmd.CommandText = $"SELECT Id, Code, Name, Price FROM products WHERE Id = @Id";

        var paramId = cmd.CreateParameter();
        paramId.ParameterName = "@Id";
        paramId.Value = id;
        cmd.Parameters.Add(paramId);

        ProductEntity? product = null;
        using IDataReader reader = cmd.ExecuteReader();
        if (reader.Read())
        {
            product = new ProductEntity
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


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Persistence/Repositories/QueryBuilderProductMSSQL.cs
```CSharp


using dbdemo.Infraestructure.Persistence.Entitites;

namespace dbdemo.Repository;

public class QueryBuilderProductMSSQL : IQueryBuilderProduct
{
    public string SelectAll(int limit)
    {
        return $"SELECT TOP ({limit}) Id, Code, Name, Price FROM products";
    }
    public string Insert(ProductEntity product)
    {
        return @"INSERT INTO products (Id, Code, Name, Price)
                            VALUES (@Id, @Code, @Name, @Price)";
    }
    public string Update(ProductEntity product)
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


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Services/Database/Interfaces/IDatabase.cs
```CSharp


using System.Data;


namespace dbdemo.Services;

public interface IDatabaseConnection {
    IDbConnection GetConnection();

}

```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Services/Database/MSSQLConnection.cs
```CSharp


using System.Data;
using Microsoft.Data.SqlClient;

namespace dbdemo.Services;

public class MSSQLConnection : IDatabaseConnection
{
    private readonly string _connectionString;

    public MSSQLConnection(string connectionString)
    {
        _connectionString = connectionString;
        Console.WriteLine($"Cadena de connexió {_connectionString}");
    }

    // Retorna una nova connexió SQL Server cada cop
    public IDbConnection GetConnection()
    {
        Console.WriteLine($"Cadena de connexió {_connectionString}");
        return new SqlConnection(_connectionString);
    }
    
}



```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Services/Database/PostgresConnection.cs
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


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Services/Database/Providers/DatabaseProvider.cs
```CSharp


namespace dbdemo.Services;
public enum DatabaseProvider
{
    MSSQL,
    Postgres
}


```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Services/Extensions/Database/DatabaseServiceExtensions.cs
```CSharp


namespace dbdemo.Services;
public static class DatabaseServiceExtensions
{
    public static IServiceCollection AddDatabase(
        this IServiceCollection services,
        IConfiguration config)
    {
        string providerName = config["Database:Provider"]
            ?? throw new Exception("Database provider not configured");

        if (!Enum.TryParse<DatabaseProvider>(providerName, true, out var provider))
            throw new Exception($"Unsupported database provider: {providerName}");

        switch (provider)
        {
            case DatabaseProvider.MSSQL:
                services.AddScoped<IDatabaseConnection>(sp =>
                    new MSSQLConnection(
                        config.GetConnectionString("MSSQL")!
                    )
                );
            break;

            case DatabaseProvider.Postgres:
                services.AddScoped<IDatabaseConnection>(sp =>
                    new PostgresConnection(
                        config.GetConnectionString("Postgres")!
                    )
                );
            break;
        }

        return services;
    }
}


```


// Nom fitxer: 23-CleanCodeLight/ADO/Infraestructure/Extensions/ProductServicesExtensions.cs
```CSharp


using dbdemo.Repository;
using dbdemo.Services;
namespace dbdemo.Extensions;

public static class ProductServicesExtensions
{
    public static IServiceCollection AddProductServices(this IServiceCollection services,
        IConfiguration config)
    {
        string providerName = config["Database:Provider"]
            ?? throw new Exception("Database provider not configured");

        if (!Enum.TryParse<DatabaseProvider>(providerName, true, out var provider))
            throw new Exception($"Unsupported database provider: {providerName}");

        switch (provider)
        {
            case DatabaseProvider.MSSQL:
                services.AddScoped<IQueryBuilderProduct, QueryBuilderProductMSSQL>();
                services.AddScoped<IProductRepo, ProductMSSQL>();
            break;

            case DatabaseProvider.Postgres:
                throw new Exception($"Not implemented");
            default:
                break;
        }
        return services;
    }
}


```


// Nom fitxer: 23-CleanCodeLight/ADO/Common/Result.cs
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


