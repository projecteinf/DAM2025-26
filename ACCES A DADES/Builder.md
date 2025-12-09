# Patró Builder

* Construcció d'objectes complexos: formats per múltiples parts.
* Separació entre 

    - què volem construir (Product), 
    - com ho construïm (Builder) 
    - ordre en la construcció (Director).

---

# Estructura bàsica del patró Builder

En la seva forma més simple, el patró Builder defineix:

* Product → l’objecte que anirem construint.
* Builder → passos necessaris per construir les parts.
* ConcreteBuilder → implementació concreta dels passos.
* Client → utilitza el Builder.

## Exemple simple per entendre l’estructura (versió mínima)

```csharp
// Producte: l’objecte que volem construir
public class Product
{
    public string PartA { get; set; } = "";
}

// Interfície del Builder
public interface IProductBuilder
{
    void BuildPartA();
    Product GetResult();
}

// Implementació concreta del Builder
public class ProductBuilder : IProductBuilder
{
    private Product _product = new Product();

    public void BuildPartA()
    {
        _product.PartA = "Part A construïda";
    }

    public Product GetResult()
    {
        return _product;
    }
}

// Client
class Program
{
    static void Main()
    {
        IProductBuilder builder = new ProductBuilder();
        builder.BuildPartA();
        Product product = builder.GetResult();

        Console.WriteLine(product.PartA);
    }
}
```

---

# Diagrama

```
             +------------------+
             |  IProductBuilder |
             +------------------+
             | + BuildPartA()   |
             | + GetResult()    |
             +------------------+
                     ^
                     |
        implements   |
                     |
+------------------+ |         +------------------+
|  ProductBuilder  |---------->       Product     |
+------------------+           +------------------+
| - _product       |           | - PartA : string |
+------------------+           +------------------+
| + BuildPartA()   |           
| + GetResult()    |
+------------------+
         ^
         |
         | usa
         |
+------------------+
|     Program      |
+------------------+
| + Main()         |
+------------------+
```

---

---

# EXEMPLE:  Construcció d’un PC

## Producte → PC

```csharp
public class PC
{
    public string CPU { get; set; } = "";
    public string GPU { get; set; } = "";
    public string RAM { get; set; } = "";
    public string Storage { get; set; } = "";
    public string PowerSupply { get; set; } = "";

    public override string ToString()
    {
        return $"PC Specs:\n" +
               $"- CPU: {CPU}\n" +
               $"- GPU: {GPU}\n" +
               $"- RAM: {RAM}\n" +
               $"- Storage: {Storage}\n" +
               $"- Power Supply: {PowerSupply}\n";
    }
}
```

---

## Interfície Builder → defineix els passos

```csharp
public interface IPCBuilder
{
    void BuildCPU();
    void BuildGPU();
    void BuildRAM();
    void BuildStorage();
    void BuildPowerSupply();

    PC GetResult();
}
```

---

## Builders Concrets

### Builder 1: PC Gaming

```csharp
public class GamingPCBuilder : IPCBuilder
{
    private PC _pc = new PC();

    public void BuildCPU()        => _pc.CPU = "Intel i9";
    public void BuildGPU()        => _pc.GPU = "NVIDIA RTX 4080";
    public void BuildRAM()        => _pc.RAM = "32GB DDR5";
    public void BuildStorage()    => _pc.Storage = "2TB NVMe SSD";
    public void BuildPowerSupply()=> _pc.PowerSupply = "850W Gold";

    public PC GetResult() => _pc;
}
```

### Builder 2: PC Oficina

```csharp
public class OfficePCBuilder : IPCBuilder
{
    private PC _pc = new PC();

    public void BuildCPU()        => _pc.CPU = "Intel i5";
    public void BuildGPU()        => _pc.GPU = "Integrada Intel UHD";
    public void BuildRAM()        => _pc.RAM = "16GB DDR4";
    public void BuildStorage()    => _pc.Storage = "512GB SSD";
    public void BuildPowerSupply()=> _pc.PowerSupply = "500W Bronze";

    public PC GetResult() => _pc;
}
```

---

## Director (opcional)

```csharp
public class PCDirector
{
    public void ConstructBasicPC(IPCBuilder builder)
    {
        builder.BuildCPU();
        builder.BuildRAM();
        builder.BuildStorage();
    }

    public void ConstructFullPC(IPCBuilder builder)
    {
        builder.BuildCPU();
        builder.BuildGPU();
        builder.BuildRAM();
        builder.BuildStorage();
        builder.BuildPowerSupply();
    }
}
```

---

## Ús del patró amb l’exemple del PC

```csharp
class Program
{
    static void Main()
    {
        var director = new PCDirector();

        // Construïm un PC Gaming complet
        IPCBuilder gamingBuilder = new GamingPCBuilder();
        director.ConstructFullPC(gamingBuilder);
        PC pcGaming = gamingBuilder.GetResult();
        Console.WriteLine("🎮 PC Gaming:");
        Console.WriteLine(pcGaming);

        // Construïm un PC d'oficina bàsic
        IPCBuilder officeBuilder = new OfficePCBuilder();
        director.ConstructBasicPC(officeBuilder);
        PC pcOffice = officeBuilder.GetResult();
        Console.WriteLine("💼 PC Oficina:");
        Console.WriteLine(pcOffice);
    }
}
```

---

# Explicació

* Separació de responsabilitats:

  * `PC` = què construïm.
  * `IPCBuilder` = com es construeix.
  * `PCDirector` = en quin ordre es construeix.

* Flexibilitat:

  * Pots crear diferents Builders (Gaming, Oficina, Econòmic…).

* Paral·lelisme amb `WebApplicationBuilder`:

  * `Product` = `WebApplication`.
  * `ConcreteBuilder` = `WebApplicationBuilder`.
  * `Director` = `Program.cs`.



