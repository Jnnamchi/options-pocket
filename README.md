# options-pocket
Stock market options API and front-end

This project is to facilitate my analysis of a stock's options landscape in order to identify trades to make.

The focus is to agglomorate a stock's:
- Share price
- Options Chain
- Implied Volatility Ranks and Percentiles

For example, if a stock's IV rank is 90%, then I might look to implement strategies that profit from a decrease in the stock's implied volatility, as the IV rank of 90% indicates that the stock's current IV is at the top of its range over the past year (for a one-year IV rank). This would likely involve writing contracts and receiving a premium, then looking to keep as much of it as possible as I'd expect the option to expire worthless at expiry.

On the other hand, if a stock's IV rank is 0%, then traders might look to implement strategies that profit from an increase in implied volatility, as the IV rank of 0% indicates the stock's current implied volatility is at the bottom of its range over the past year. This would look like purchasing extremely cheap options expecting their value to rise as volatility increases back to its mean.