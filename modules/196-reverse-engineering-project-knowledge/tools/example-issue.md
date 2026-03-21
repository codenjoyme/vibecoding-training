# Example Issue: Add User Notification Preferences API

**Issue #47**

## Description

Users need the ability to manage their notification preferences. Currently, all users receive all notification types (email, in-app, SMS) with no way to opt out of specific channels or event types.

## Requirements

- Add a REST endpoint to get current notification preferences for a user
- Add a REST endpoint to update notification preferences
- Preferences should cover: email, in-app push, and SMS channels
- Each channel can be toggled independently for these event types:
  - Order status updates
  - Marketing promotions
  - Security alerts (cannot be disabled)
- Default new users to all notifications enabled
- Changes should take effect immediately

## Acceptance Criteria

- [ ] GET `/api/users/{userId}/notification-preferences` returns current prefs
- [ ] PUT `/api/users/{userId}/notification-preferences` updates prefs
- [ ] Security alerts cannot be disabled via API (server enforces this)
- [ ] Preferences are persisted in the database
- [ ] Unit tests cover all preference combinations
- [ ] API documentation is updated
