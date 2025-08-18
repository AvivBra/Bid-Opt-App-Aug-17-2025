# איפיון עמוד Campaigns Optimizer

## 1. סקירה כללית

### מטרת העמוד
עמוד לביצוע Negation ו-Harvesting על קמפיינים.

### סטטוס
**TBD - יפותח בשלבים 5-6**

## 2. Page Structure (Future)

```python
def render_campaigns_optimizer_page():
    """Main page for Campaigns Optimizer - TBD"""
    
    # Page title
    st.markdown("<h1 style='text-align: center;'>CAMPAIGNS OPTIMIZER</h1>", 
                unsafe_allow_html=True)
    
    # Placeholder for future development
    st.info("Campaigns Optimizer will be available in Phase 5-6")
    
    # Future structure (commented out)
    """
    # Section 1: Select Processing Types
    render_processing_types_section()
    
    # Section 2: Upload Files
    render_campaigns_upload_section()
    
    # Section 3: Data Validation
    if has_campaign_files():
        render_campaigns_validation_section()
    
    # Section 4: Output Files
    if st.session_state.get('campaigns_processing_status') == 'complete':
        render_campaigns_output_section()
    """
```

## 3. Select Processing Types Section (TBD)

### Layout Mockup
```python
def render_processing_types_section():
    """Render processing type selection - TBD"""
    
    with st.container():
        st.markdown(
            """
            <div class='section-container'>
                <h2 class='section-header'>SELECT PROCESSING TYPES</h2>
            """,
            unsafe_allow_html=True
        )
        
        # Checkbox list for Negation and Harvesting
        processing_types = {
            'negation': 'Negation',
            'harvesting': 'Harvesting'
        }
        
        selected = []
        for key, label in processing_types.items():
            if st.checkbox(label, key=f"proc_{key}"):
                selected.append(key)
        
        st.session_state.selected_processes = selected
        
        st.markdown("</div>", unsafe_allow_html=True)
```

## 4. Upload Section (TBD)

### Similar Structure to Bid Optimizer
```python
def render_campaigns_upload_section():
    """Upload section for campaigns - TBD"""
    
    # Same upload buttons as Bid Optimizer
    # Template, Bulk 7/30/60, Data Rova
    # But different validation rules
    pass
```

## 5. Negation Logic (TBD)

### Placeholder
```python
class NegationOptimization:
    """
    TBD - Negation optimization logic
    Will be defined in Phase 5
    """
    
    def process(self, bulk_df, template_df):
        """Process negation - TBD"""
        pass
```

## 6. Harvesting Logic (TBD)

### Placeholder
```python
class HarvestingOptimization:
    """
    TBD - Harvesting optimization logic
    Will be defined in Phase 6
    """
    
    def process(self, bulk_df, template_df):
        """Process harvesting - TBD"""
        pass
```

## 7. Future Requirements

### Expected Features
- Similar UI to Bid Optimizer
- Same file upload mechanism
- Different processing logic
- Different output structure

### Files Required (TBD)
- Template with Port Values and Top ASINs
- Specific Bulk files
- Possibly Data Rova integration

## 8. State Management (TBD)

### Separate State Namespace
```python
# Future state structure
campaigns_state = {
    'selected_processes': [],
    'campaigns_template_file': None,
    'campaigns_bulk_files': {},
    'campaigns_output_files': {},
    'campaigns_processing_status': 'idle'
}
```

## 9. Integration Points

### Shared Components
- Same UI components as Bid Optimizer
- Same file upload mechanism
- Same progress indicators
- Same download functionality

### Different Logic
- Different validation rules
- Different processing algorithms
- Different output formats

## 10. Development Timeline

### Phase 5: Negation
- Define Negation logic
- Implement validation
- Create output format
- Test with sample data

### Phase 6: Harvesting  
- Define Harvesting logic
- Implement validation
- Create output format
- Test with sample data
- Full integration testing