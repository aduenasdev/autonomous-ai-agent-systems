class WeatherTool:
    def run(self, user_input: str) -> str:
        # Very small simulated weather database
        samples = {
            'london': '15°C, Cloudy',
            'new york': '22°C, Sunny',
            'mumbai': '30°C, Humid',
            'tokyo': '18°C, Light rain'
        }
        import re, random
        m = re.search(r'in\s+([A-Za-z ]+)', user_input, flags=re.IGNORECASE)
        city = None
        if m:
            city = m.group(1).strip().lower()
        else:
            words = user_input.split()
            if words:
                city = words[-1].strip('?.!,').lower()
        if city and city in samples:
            return f"Weather in {city.title()}: {samples[city]} (simulated)"
        city_guess = city.title() if city else 'Unknown City'
        temp = random.randint(10,35)
        cond = random.choice(['Sunny','Cloudy','Light rain','Clear','Humid'])
        return f"Weather in {city_guess}: {temp}°C, {cond} (simulated)"
