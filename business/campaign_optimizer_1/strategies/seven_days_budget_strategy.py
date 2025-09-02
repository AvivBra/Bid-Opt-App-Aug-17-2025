import pandas as pd
import numpy as np
from ..constants import (
    ACOS_THRESHOLD, BUDGET_MINIMUM, BUDGET_MEDIUM, BUDGET_HIGH,
    OPERATION_UPDATE, COL_UNITS, COL_ACOS, COL_DAILY_BUDGET, COL_OPERATION
)

class SevenDaysBudgetStrategy:
    """
    Implements the 4-step budget optimization logic for Campaign Optimizer 1:
    
    Step 1: Units = 0 AND Daily Budget > 1 → Daily Budget = 1
    Step 2: Units > 0 AND ACOS > 0.17 AND Daily Budget > 1 → Daily Budget = 1  
    Step 3: Units > 0 AND ACOS < 0.17 AND Daily Budget < 3 → Daily Budget = 3
    Step 4: Units > 2 AND ACOS < 0.17 AND Daily Budget < 5 → Daily Budget = 5
    """
    
    def optimize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply 4-step budget optimization logic to campaign data.
        
        Args:
            df: DataFrame with campaign data
            
        Returns:
            DataFrame with optimized budgets and Operation column set
        """
        # Work on a copy to avoid modifying original data
        result_df = df.copy()
        
        # Initialize Operation column with NaN
        result_df[COL_OPERATION] = np.nan
        
        # Apply optimization steps in sequence
        result_df = self._apply_step_1(result_df)
        result_df = self._apply_step_2(result_df) 
        result_df = self._apply_step_3(result_df)
        result_df = self._apply_step_4(result_df)
        
        return result_df
    
    def _apply_step_1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 1: if (Units = 0 & Daily Budget > 1) then set Daily Budget = 1, Operation = update
        """
        mask = (df[COL_UNITS] == 0) & (df[COL_DAILY_BUDGET] > BUDGET_MINIMUM)
        df.loc[mask, COL_DAILY_BUDGET] = BUDGET_MINIMUM
        df.loc[mask, COL_OPERATION] = OPERATION_UPDATE
        return df
    
    def _apply_step_2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 2: if (Units > 0 & ACOS > 0.17 & Daily Budget > 1) then set Daily Budget = 1, Operation = update
        """
        mask = (df[COL_UNITS] > 0) & (df[COL_ACOS] > ACOS_THRESHOLD) & (df[COL_DAILY_BUDGET] > BUDGET_MINIMUM)
        df.loc[mask, COL_DAILY_BUDGET] = BUDGET_MINIMUM
        df.loc[mask, COL_OPERATION] = OPERATION_UPDATE
        return df
    
    def _apply_step_3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 3: if (Units > 0 & ACOS < 0.17 & Daily Budget < 3) then set Daily Budget = 3, Operation = update
        """
        mask = (df[COL_UNITS] > 0) & (df[COL_ACOS] < ACOS_THRESHOLD) & (df[COL_DAILY_BUDGET] < BUDGET_MEDIUM)
        df.loc[mask, COL_DAILY_BUDGET] = BUDGET_MEDIUM
        df.loc[mask, COL_OPERATION] = OPERATION_UPDATE
        return df
    
    def _apply_step_4(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 4: if (Units > 2 & ACOS < 0.17 & Daily Budget < 5) then set Daily Budget = 5, Operation = update
        """
        mask = (df[COL_UNITS] > 2) & (df[COL_ACOS] < ACOS_THRESHOLD) & (df[COL_DAILY_BUDGET] < BUDGET_HIGH)
        df.loc[mask, COL_DAILY_BUDGET] = BUDGET_HIGH
        df.loc[mask, COL_OPERATION] = OPERATION_UPDATE
        return df