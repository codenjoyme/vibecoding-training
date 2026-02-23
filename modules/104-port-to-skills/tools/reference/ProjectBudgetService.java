package com.example.projectmanager.service;

import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Service for project budget calculations.
 * Used internally by ProjectController REST endpoints.
 *
 * NOTE: This is the canonical source of budget calculation logic.
 * All calculation rules, rounding behavior, and edge case handling
 * are defined here. Downstream clients (CLI tools, scripts, reports)
 * must reproduce this logic exactly.
 */
@Service
public class ProjectBudgetService {

    /**
     * Calculate total project cost including labor and overhead.
     *
     * Assumes 8 working hours per person per day.
     * Overhead is calculated as a percentage of labor cost only (not total).
     *
     * @param teamSize      number of team members
     * @param hourlyRate    cost per person per hour (USD)
     * @param durationDays  project duration in working days
     * @param overheadPct   overhead percentage (e.g. 20 for 20%)
     * @return ProjectCostResult with labor, overhead, and total cost
     */
    public ProjectCostResult calculateProjectCost(
            int teamSize, double hourlyRate, int durationDays, double overheadPct) {

        double totalHours = teamSize * durationDays * 8.0;
        double laborCost = round(totalHours * hourlyRate);
        double overheadCost = round(laborCost * overheadPct / 100.0);
        double totalCost = round(laborCost + overheadCost);

        return new ProjectCostResult(totalHours, laborCost, overheadCost, totalCost);
    }

    /**
     * Calculate Return on Investment (ROI) as a percentage.
     *
     * Formula: ROI = (netProfit / investment) * 100
     * Result is rounded to 2 decimal places.
     *
     * @param investment  total investment amount (USD)
     * @param netProfit   net profit generated (USD, may be negative)
     * @return ROI as a percentage (e.g. 25.0 means 25%)
     * @throws IllegalArgumentException if investment is zero
     */
    public double calculateROI(double investment, double netProfit) {
        if (investment == 0) {
            throw new IllegalArgumentException("Investment cannot be zero");
        }
        return round((netProfit / investment) * 100.0);
    }

    /**
     * Calculate project burn rate and budget forecast.
     *
     * Daily burn rate = spentSoFar / daysElapsed
     * Projected total = dailyBurnRate * totalDays
     * Days until budget empty = remainingBudget / dailyBurnRate
     *
     * @param budget        total approved budget (USD)
     * @param spentSoFar    amount spent to date (USD)
     * @param daysElapsed   working days elapsed since project start
     * @param totalDays     total project duration in working days
     * @return BurnRateResult with daily rate, projection, and risk flags
     * @throws IllegalArgumentException if daysElapsed is zero
     */
    public BurnRateResult calculateBurnRate(
            double budget, double spentSoFar, int daysElapsed, int totalDays) {

        if (daysElapsed == 0) {
            throw new IllegalArgumentException("Days elapsed cannot be zero");
        }

        double dailyBurnRate = round(spentSoFar / daysElapsed);
        double projectedTotal = round(dailyBurnRate * totalDays);
        double remainingBudget = round(budget - spentSoFar);
        int daysUntilEmpty = (int) (remainingBudget / dailyBurnRate);
        boolean overBudget = projectedTotal > budget;

        return new BurnRateResult(dailyBurnRate, projectedTotal, remainingBudget,
                daysUntilEmpty, overBudget);
    }

    // --- Utility ---

    private double round(double value) {
        return BigDecimal.valueOf(value)
                .setScale(2, RoundingMode.HALF_UP)
                .doubleValue();
    }

    // --- Result classes ---

    public static class ProjectCostResult {
        public final double totalHours;
        public final double laborCost;
        public final double overheadCost;
        public final double totalCost;

        public ProjectCostResult(double totalHours, double laborCost,
                                  double overheadCost, double totalCost) {
            this.totalHours = totalHours;
            this.laborCost = laborCost;
            this.overheadCost = overheadCost;
            this.totalCost = totalCost;
        }
    }

    public static class BurnRateResult {
        public final double dailyBurnRate;
        public final double projectedTotal;
        public final double remainingBudget;
        public final int daysUntilEmpty;
        public final boolean overBudget;

        public BurnRateResult(double dailyBurnRate, double projectedTotal,
                               double remainingBudget, int daysUntilEmpty, boolean overBudget) {
            this.dailyBurnRate = dailyBurnRate;
            this.projectedTotal = projectedTotal;
            this.remainingBudget = remainingBudget;
            this.daysUntilEmpty = daysUntilEmpty;
            this.overBudget = overBudget;
        }
    }
}
