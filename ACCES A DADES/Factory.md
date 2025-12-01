# Patró Factory

```csharp
public interface IEngine
{
    void Start();
}
```

## Implementacions concretes

```csharp
public class ElectricEngine : IEngine
{
    public void Start()
    {
        Console.WriteLine("Arranquem el motor elèctric.");
    }
}

public class GasoilEngine : IEngine
{
    public void Start()
    {
        Console.WriteLine("Arranquem el motor a gasoil.");
    }
}
```

## Classe dependent (`Car`)

```csharp
public class Car
{
    private readonly IEngine _engine;

    public Car(IEngine engine)
    {
        _engine = engine;
    }

    public void StartCar()
    {
        _engine.Start();
    }
}
```

## Interface de Factory

```csharp
public interface IEngineFactory
{
    IEngine CreateEngine();
}
```

## Fàbriques concretes (una per tipus de motor)

- Cada tipus de motor tindrà la seva fàbrica que sap com crear-lo:

```csharp
public class ElectricEngineFactory : IEngineFactory
{
    public IEngine CreateEngine()
    {
        return new ElectricEngine();
    }
}

public class GasoilEngineFactory : IEngineFactory
{
    public IEngine CreateEngine()
    {
        return new GasoilEngine();
    }
}
```

## Programa principal amb injecció de la fàbrica

- Decideix quina fàbrica utilitzar, no quin motor crear.

```csharp
class Program
{
    static void Main()
    {
        Console.WriteLine("Tria el tipus de motor (electric / gasoil):");
        string type = Console.ReadLine()?.ToLower() ?? "electric";

        IEngineFactory factory = type switch
        {
            "electric" => new ElectricEngineFactory(),
            "gasoil"   => new GasoilEngineFactory(),
            _ => throw new ArgumentException("Tipus de motor desconegut.")
        };

        IEngine engine = factory.CreateEngine();
        Car car = new Car(engine);

        car.StartCar();
    }
}
```
