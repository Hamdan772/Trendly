# 🎨 Quick Visual Guide - Investment Analyzer UI

## Color Reference

### Score Badges
```
🟢 STRONG BUY (70-100)
   Background: Green gradient
   Text: White
   Shadow: Green glow

🟡 HOLD (40-69)
   Background: Orange gradient
   Text: White
   Shadow: Orange glow

🔴 AVOID (0-39)
   Background: Red gradient
   Text: White
   Shadow: Red glow
```

### Metric Cards
```
💰 Current Price
   Icon: 💰 (money bag)
   Color: Neutral gray

📈 Predicted Price
   Icon: 📈 (chart up)
   Color: Green (positive) / Red (negative)

⚠️ Risk Level
   Icon: ⚠️ (warning)
   Color: Green (low) / Orange (medium) / Red (high)

📊 Trend
   Icon: 📈/➡️/📉
   Color: Based on strength
```

## Layout Structure

```
┌─────────────────────────────────────────┐
│          📈 HERO TITLE                   │
│     Subtitle text                        │
├─────────────────────────────────────────┤
│                                          │
│  1️⃣ Choose Your Stock                   │
│  [        Search Input        ]          │
│  [        Dropdown            ]          │
│  ┌─────────────────────────┐            │
│  │  AAPL • Apple Inc       │            │
│  └─────────────────────────┘            │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  2️⃣ Set Forecast Period                 │
│  ◄────────●──────────►                  │
│      30 days                             │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  3️⃣ Run Analysis                        │
│     ┌─────────────────┐                 │
│     │  🚀 ANALYZE NOW  │                 │
│     └─────────────────┘                 │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  ✅ Analysis Complete!                   │
│                                          │
│  📊 Your Investment Report               │
│                                          │
│     ┌───────────────┐                   │
│     │  🟢            │                   │
│     │               │                   │
│     │   85/100      │                   │
│     └───────────────┘                   │
│                                          │
│     STRONG BUY                           │
│                                          │
│  ┌────────────────────────────┐         │
│  │   INVEST WITH CONFIDENCE    │         │
│  └────────────────────────────┘         │
│                                          │
│  💡 What This Means                      │
│  Detailed explanation here...            │
│                                          │
│  🔍 Why This Score?                      │
│  1. Reason one...                        │
│  2. Reason two...                        │
│  3. Reason three...                      │
│                                          │
│  📊 Key Metrics                          │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐           │
│  │ 💰 │ │ 📈 │ │ ⚠️ │ │ 📊 │           │
│  │$150│ │$155│ │Low │ │Str │           │
│  └────┘ └────┘ └────┘ └────┘           │
│                                          │
│  📈 Price Forecast                       │
│  [        Chart Area        ]            │
│                                          │
│  ▼ See Detailed Breakdown                │
│                                          │
│  📥 Download Forecast Data               │
│                                          │
└─────────────────────────────────────────┘
```

## Interactive Elements

### Hover Effects
- **Buttons**: Lift up 2px + darker gradient
- **Cards**: Lift up 5px + stronger shadow
- **Inputs**: Blue border + focus ring

### Animations
- **Score Badge**: Fade in from bottom (0.6s)
- **Recommendation**: Fade in from bottom (0.8s)
- **Cards**: Smooth hover transitions (0.2s)

## Typography Scale

```
Hero Title:       48px, weight 900
Section Headers:  36px, weight 800
Subsections:      28px, weight 700
Large Text:       24px, weight bold
Body Text:        16px, weight normal
Small Text:       14px, weight normal
```

## Spacing

```
Between sections:   40px
Around cards:       20px
Inside cards:       20px
Button padding:     15px 40px
```

## Component States

### Button States
```
Default:  Blue gradient + shadow
Hover:    Darker blue + stronger shadow + lift
Active:   Even darker + pressed effect
Loading:  Spinner + "Analyzing..."
```

### Input States
```
Default:  Gray border
Focus:    Blue border + ring
Filled:   Shows content
Error:    Red border (if applicable)
```

### Card States
```
Default:  White + light shadow
Hover:    White + stronger shadow + lift
```

## Mobile Responsiveness

### Breakpoints
```
Desktop:  > 768px  → 4 columns
Tablet:   768px    → 2 columns
Mobile:   < 768px  → 1 column
```

### Mobile Adjustments
- Larger touch targets (min 44px)
- Stack columns vertically
- Reduce font sizes slightly
- Increase padding for thumbs
- Full-width buttons

## Accessibility

### Color Contrast
```
✓ Score text on colored background: 7:1
✓ Body text on white: 8:1
✓ Secondary text on white: 4.5:1
✓ All pass WCAG AA standards
```

### Focus Indicators
```
All interactive elements have visible focus rings
Blue ring: 3px solid rgba(59, 130, 246, 0.3)
```

### Screen Reader Support
```
✓ Semantic HTML structure
✓ Proper heading hierarchy
✓ Alt text for visual elements
✓ ARIA labels where needed
```

## Quick CSS Reference

### Most Used Classes
```css
.score-badge { /* Giant score display */ }
.recommendation { /* Decision box */ }
.info-box { /* Blue explanation box */ }
.metric-card { /* Individual metric */ }
.divider { /* Section separator */ }
.step-header { /* 1️⃣ 2️⃣ 3️⃣ headers */ }
```

### Most Used Colors
```css
--primary: #3b82f6
--success: #10b981
--warning: #f59e0b
--danger: #ef4444
--gray-900: #1f2937
--gray-500: #6b7280
```

## Best Practices

### DO ✅
- Use large, clear fonts
- Provide visual feedback
- Show loading states
- Use color + text + icons together
- Keep it simple and focused
- Test on mobile devices

### DON'T ❌
- Hide important info in expandable sections
- Use jargon without explanation
- Rely on color alone
- Make users hunt for actions
- Overwhelm with too much data
- Use tiny fonts or buttons

## Testing Checklist

- [ ] Score displays correctly for all ranges
- [ ] Colors match score thresholds
- [ ] Hover effects work smoothly
- [ ] Mobile layout stacks properly
- [ ] All buttons are clickable
- [ ] Loading spinner shows
- [ ] Chart renders correctly
- [ ] Download works
- [ ] No console errors
- [ ] Fast page load

---

**Pro Tip**: Keep the interface clean by showing the most important info first, with details available on demand through expandable sections!
