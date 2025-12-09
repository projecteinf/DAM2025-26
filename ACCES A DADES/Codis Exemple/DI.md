# Dependence Injection

```CSharp
public interface IEngine
{
    void Start();
}
```

```CSharp
public class ElectricEngine : IEngine
{
    public void Start()
    {
        Console.WriteLine("Arranquem el motor elèctric.");
    }
}
```

- Classe concreta motor a gas: GasoilEngine 

```CSharp
public class GasoilEngine : IEngine
{
    public void Start()
    {
        Console.WriteLine("Arranquem el motor a gas.");
    }
}
```

- Classe Car (dependent)

```CSharp
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

- Programa principal.  

```CSharp
class Program
{
    static void Main()
    {
        IEngine engine = new GasEngine();

        Car car = new Car(engine);

        // Fem servir el cotxe
        car.StartCar();  // Imprimeix: The gas engine starts!
    }
}

```
