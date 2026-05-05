# 1. Create a numeric vector
sales=c(100, 200, 150, 300, 250)

# Summary statistics
summary(sales)

# Frequency table (for categorical-like values)
table(sales)


# 2. Create a factor (categorical data)
region=factor(c("North", "South", "East", "West", "North"))

# View factor summary
summary(region)


# 3. Create a data frame
df=data.frame(
  Product = c("A", "B", "C", "D", "E"),
  Sales = sales,
  Region = region
)

# View data frame
print(df)


# Explore numeric vs categorical
summary(df)
table(df$Region)


# 4. Create reusable function for statistics
compute_stats=function(x) {
  cat("Mean:", mean(x), "\n")
  cat("Median:", median(x), "\n")
  cat("Standard Deviation:", sd(x), "\n")
  cat("Min:", min(x), "\n")
  cat("Max:", max(x), "\n")
}

# Call function
compute_stats(sales)