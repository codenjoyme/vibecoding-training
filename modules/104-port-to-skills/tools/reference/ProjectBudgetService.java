package com.example.demo.service;

import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Core tools service — the same three operations exposed in Module 100 (MCP)
 * and Module 103 (REST/CLI): echo, get_time, and calculate.
 *
 * NOTE: This is the canonical source of tool logic.
 * All formatting rules, operation behavior, and edge case handling
 * are defined here. Downstream clients (CLI scripts, MCP servers)
 * must reproduce this logic exactly.
 */
@Service
public class ToolsService {

    /**
     * Echo the input text back with a prefix.
     *
     * Output format: "Echo: {text}"
     * This is intentionally trivial — used to verify the tool pipeline works end-to-end.
     *
     * @param text  any non-null string
     * @return "Echo: " + text
     */
    public String echo(String text) {
        return "Echo: " + text;
    }

    /**
     * Return the current server timestamp as a formatted string.
     *
     * Output format: "Current time: yyyy-MM-dd HH:mm:ss"
     * Uses the server's local timezone (no UTC conversion).
     *
     * @return formatted current datetime string
     */
    public String getTime() {
        String formatted = LocalDateTime.now()
                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        return "Current time: " + formatted;
    }

    /**
     * Perform a basic arithmetic operation on two numbers.
     *
     * Supported operations: add, subtract, multiply, divide
     * Output format: "Result: {a} {operation} {b} = {result}"
     * Result is a double; no rounding is applied.
     *
     * @param a          first operand
     * @param b          second operand
     * @param operation  one of: "add", "subtract", "multiply", "divide"
     * @return formatted result string
     * @throws IllegalArgumentException if operation is unknown or b is zero for divide
     */
    public String calculate(double a, double b, String operation) {
        double result;
        switch (operation) {
            case "add":      result = a + b; break;
            case "subtract": result = a - b; break;
            case "multiply": result = a * b; break;
            case "divide":
                if (b == 0) throw new IllegalArgumentException("Division by zero");
                result = a / b;
                break;
            default:
                throw new IllegalArgumentException(
                    "Unknown operation: " + operation +
                    ". Allowed: add, subtract, multiply, divide");
        }
        return String.format("Result: %s %s %s = %s", a, operation, b, result);
    }
}
