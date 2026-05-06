/**
 * IRRIGATION PLANNING FEATURE - FRONTEND DISPLAY
 * 
 * Added new tab "Irrigation Planning" to the Results page
 * 
 * FEATURES DISPLAYED:
 * 
 * 1. SUMMARY CARDS (4-column grid)
 *    - Irrigation Method
 *    - Water Efficiency %
 *    - Additional Water Needed (mm)
 *    - Cost per Acre (Rs.)
 * 
 * 2. WATER REQUIREMENT ANALYSIS
 *    - Total Water Needed (mm)
 *    - Available Rainfall (mm) 
 *    - Additional Irrigation Required (mm) [highlighted]
 * 
 * 3. IRRIGATION SCHEDULE (Stage-by-Stage)
 *    For each stage displays:
 *    - Stage Name (e.g., "Seedling", "Flowering", etc.)
 *    - Days after sowing range
 *    - Irrigation depth per application (mm)
 *    - Frequency (e.g., "Every 5-7 days")
 *    - Important notes for that stage
 * 
 * 4. COST & EFFICIENCY SUMMARY
 *    Left Card - Irrigation Cost:
 *    - Cost per acre
 *    - Estimated total cost calculation
 *    
 *    Right Card - Water Use Efficiency:
 *    - Efficiency percentage with progress bar
 *    - Explanation of water loss reduction
 * 
 * 5. WATER MANAGEMENT TIPS
 *    - Soil-specific recommendations
 *    - Budget-aware suggestions
 *    - Best practices list
 *    - Each tip with icon and description
 * 
 * EXAMPLE DATA STRUCTURE:
 * 
 * results.irrigation_planning = {
 *   irrigation_required_mm: 0.0,
 *   total_water_needed_mm: 600.0,
 *   rainfall_mm: 700.0,
 *   irrigation_method: "Drip Irrigation (Widely spaced crops)",
 *   efficiency_percentage: 90,
 *   estimated_cost_per_acre: 814.00,
 *   irrigation_schedule: [
 *     {
 *       stage: "Seedling to Branching",
 *       days_after_sowing: "0-45",
 *       depth_mm: 35,
 *       frequency: "Every 7-10 days",
 *       notes: "Light irrigation, good drainage essential"
 *     },
 *     {
 *       stage: "Flowering & Boll Formation",
 *       days_after_sowing: "45-120",
 *       depth_mm: 45,
 *       frequency: "Every 10-15 days",
 *       notes: "Most critical - 4-6 irrigations"
 *     },
 *     ...more stages
 *   ],
 *   water_management_tips: [
 *     "High water requirement crop - Plan for reliable water source",
 *     "Consider water harvesting or pond construction",
 *     "Install efficient drip irrigation to reduce water wastage",
 *     ...more tips
 *   ]
 * }
 * 
 * DISPLAY FLOW:
 * 
 * User clicks "Irrigation Planning" tab in Results page
 *           ↓
 * Tab content loads showing:
 *   • Summary stats grid (4 cards)
 *   • Water requirement breakdown
 *   • Complete irrigation schedule (4+ stages)
 *   • Cost analysis
 *   • Efficiency visualization
 *   • Water management best practices
 * 
 * STYLING:
 * - Blue/Cyan/Green color scheme for water-related content
 * - Card-based layout for clarity
 * - Progress bar for efficiency visualization
 * - Color-coded severity badges
 * - Icons for visual hierarchy
 * - Responsive grid (1 col mobile, 2 col tablet+)
 * 
 * RESPONSIVE DESIGN:
 * - Mobile: Single column for all sections
 * - Tablet/Desktop: 2-column layout for cost/efficiency cards
 * - All text properly sized and readable
 * - Touch-friendly card spacing
 */
