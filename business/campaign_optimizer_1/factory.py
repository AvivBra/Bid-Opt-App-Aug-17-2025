from .strategies.seven_days_budget_strategy import SevenDaysBudgetStrategy

class CampaignOptimizer1Factory:
    """
    Factory for creating Campaign Optimizer 1 strategies.
    """
    
    @staticmethod
    def create_seven_days_budget_strategy():
        """Create and return SevenDaysBudgetStrategy instance."""
        return SevenDaysBudgetStrategy()
    
    @staticmethod
    def get_available_strategies():
        """Return list of available strategy names."""
        return ["seven_days_budget"]