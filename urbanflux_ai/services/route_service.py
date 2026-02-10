import random

class RouteService:
    def analyze(self):
        routes = ['direct', 'warehouse']
        rec = random.choice(routes)
        
        freshness_impact = 74 if rec == 'warehouse' else 85
        
        return {
            "recommended_route": rec,
            "expected_freshness": freshness_impact,
            "confidence": 0.87
        }
