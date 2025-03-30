import asyncio
from typing import List, Optional
from pydantic import BaseModel
from async_promptic import llm, Promptic


# Define a Pydantic model for return type
class WeatherInfo(BaseModel):
    temperature: float
    conditions: str
    recommendation: str


class CityInfo(BaseModel):
    population: int
    description: str


class TravelAssistant:
    """A class that demonstrates using @llm decorator with class methods and Pydantic models"""
    
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.request_count = 0
    
    # Test class method with Pydantic return type and tools, with only self parameter
    @llm(model="gpt-3.5-turbo")
    async def get_random_city_weather(self) -> WeatherInfo:
        """
        You are a travel assistant.
        Choose a random interesting city and provide weather information for it.
        Use the fetch_weather tool to get weather data for your chosen city.
        Format your response as a WeatherInfo object.
        """
        self.request_count += 1
        print(f"Processing random city weather request #{self.request_count}")
        # This method doesn't use _result parameter
    
    # Register an async tool with the class method
    @get_random_city_weather.tool
    async def fetch_weather(self, city):
        """
        Fetches weather data for a city
        """
        print(f"Fetching weather for {city}...")
        await asyncio.sleep(1)  # Simulate API call
        return f"Sunny and 75°F in {city}"
    
    # Test class method with Pydantic return type and tools, with additional params
    @llm(model="gpt-3.5-turbo")
    async def get_city_weather(self, city: str) -> WeatherInfo:
        """
        You are a travel assistant.
        Provide weather information for {city}.
        Use the fetch_city_info tool to get information about the city.
        Use the fetch_weather tool to get weather data for the city.
        Format your response as a WeatherInfo object.
        """
        self.request_count += 1
        print(f"Processing weather request #{self.request_count} for {city}")
        # This method doesn't use _result parameter
    
    # Register tools for the city_weather method
    @get_city_weather.tool
    async def fetch_city_info(self, city: str) -> CityInfo:
        """
        Fetches information about a city
        """
        print(f"Fetching info for {city}...")
        await asyncio.sleep(0.5)  # Simulate API call
        
        # Return a CityInfo object for demonstration
        return CityInfo(
            population=500000,
            description=f"{city} is a beautiful city with lots to see and do."
        )
    
    @get_city_weather.tool
    async def fetch_weather(self, city: str):
        """
        Fetches weather data for a city
        """
        print(f"Fetching weather for {city}...")
        await asyncio.sleep(0.5)  # Simulate API call
        return f"Sunny and 75°F in {city}"
    
    # Test class method with Pydantic return type and _result parameter
    @llm(model="gpt-3.5-turbo")
    async def get_city_recommendation(self, preferences: str, _result: Optional[WeatherInfo] = None) -> WeatherInfo:
        """
        You are a travel assistant.
        Based on these preferences: '{preferences}',
        recommend a suitable city and its weather.
        Use the fetch_weather tool to get weather for your recommended city.
        Format your response as a WeatherInfo object.
        """
        self.request_count += 1
        print(f"Processing recommendation request #{self.request_count} for preferences: {preferences}")
        print(f"LLM result type: {type(_result)}")
        return _result  # Return the parsed Pydantic model


    @get_city_recommendation.tool
    async def fetch_weather(self, city: str):
        """
        Fetches weather data for a city
        """
        print(f"Fetching weather for {city}...")
        await asyncio.sleep(0.5)  # Simulate API call
        return f"Sunny and 75°F in {city}"


async def main():
    assistant = TravelAssistant()
    
    # Test class method with only self parameter
    print("\n=== Testing class method with only self parameter ===")
    try:
        random_city_weather = await assistant.get_random_city_weather()
        print(f"Type: {type(random_city_weather)}")
        print(f"Random city weather: {random_city_weather}")
    except Exception as e:
        print(f"Error with random city weather: {e}")
    
    # Test class method with additional parameters
    print("\n=== Testing class method with additional parameters ===")
    try:
        paris_weather = await assistant.get_city_weather("Paris")
        print(f"Type: {type(paris_weather)}")
        print(f"Paris weather: {paris_weather}")
    except Exception as e:
        print(f"Error with city weather: {e}")
    
    # Test class method with _result parameter
    print("\n=== Testing class method with _result parameter ===")
    try:
        recommendation = await assistant.get_city_recommendation("I enjoy warm weather and beaches")
        print(f"Type: {type(recommendation)}")
        print(f"Recommendation: {recommendation}")
    except Exception as e:
        print(f"Error with recommendation: {e}")


if __name__ == "__main__":
    asyncio.run(main())
