# Property Owner Registration Feature

## Overview
This document explains the new property owner registration feature that allows property owners to create accounts that require administrator approval before they can log in.

## Feature Components

### 1. Registration Page
- **File**: `frontend/public/register.html`
- **URL**: Accessible from the login page
- **Functionality**: Allows property owners to create new accounts

### 2. Backend API
- **Endpoint**: `POST /api/users/`
- **Permissions**: Public access for registration
- **Validation**: Ensures proper role assignment and approval status

### 3. Login Integration
- **File**: `frontend/public/login.html`
- **Link**: Added link to registration page
- **Approval Check**: Prevents unapproved users from logging in

## Registration Flow

### 1. Property Owner Registration
1. Property owner visits `register.html`
2. Fills out registration form (username, email, password)
3. Submits form to create account
4. Account is automatically set to:
   - Role: `property_owner`
   - Approved: `False`

### 2. Administrator Approval
1. Admin logs into admin dashboard
2. Navigates to property owners management
3. Reviews pending registrations
4. Approves or rejects accounts

### 3. Property Owner Login
1. Approved property owner visits `login.html`
2. Enters credentials
3. Successfully logs in to property owner dashboard

## Security Features

### 1. Role Enforcement
- Property owners cannot set their own role
- All new registrations are forced to `property_owner` role
- Role field is read-only in the API

### 2. Approval Process
- New accounts default to `is_approved = False`
- Unapproved users cannot log in
- Approval field is read-only in the API

### 3. Password Security
- Passwords are properly hashed using Django's built-in methods
- Password field is write-only in the API

## API Endpoints

### User Registration
- **Method**: `POST`
- **URL**: `/api/users/`
- **Permissions**: Public (no authentication required)
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "test_owner",
    "email": "test@example.com",
    "role": "property_owner",
    "is_approved": false,
    "created_at": "2025-11-28T12:00:00Z",
    "updated_at": "2025-11-28T12:00:00Z"
  }
  ```

### User Login
- **Method**: `POST`
- **URL**: `/api/users/login/`
- **Permissions**: Public
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "token": "string",
    "user": {
      "id": 1,
      "username": "test_owner",
      "email": "test@example.com",
      "role": "property_owner",
      "is_approved": true,
      "created_at": "2025-11-28T12:00:00Z",
      "updated_at": "2025-11-28T12:00:00Z"
    }
  }
  ```
- **Response (Unapproved Account)**:
  ```json
  {
    "error": "Account pending approval by administrator"
  }
  ```

## Files Created/Modified

### New Files
1. `frontend/public/register.html` - Registration page
2. `frontend/test-registration.html` - Test page
3. `REGISTRATION_FEATURE.md` - This documentation

### Modified Files
1. `frontend/public/login.html` - Added registration link
2. `backend/property_management/apps/users/views.py` - Updated permissions and login logic
3. `backend/property_management/apps/users/serializers.py` - Updated serializer security

## Testing the Feature

### 1. Test Registration
1. Open `frontend/test-registration.html` in browser
2. Click "Test Registration API" button
3. Verify successful user creation with proper role and approval status

### 2. Manual Registration Test
1. Open `frontend/public/register.html` in browser
2. Fill out registration form
3. Submit and verify success message

### 3. Login Test (Unapproved)
1. Open `frontend/public/login.html` in browser
2. Try to log in with newly registered credentials
3. Verify "Account pending approval" error

### 4. Administrator Approval Test
1. Log in as admin
2. Approve the test user through the admin interface
3. Try logging in again with the same credentials
4. Verify successful login

## Future Enhancements

### 1. Email Notifications
- Send confirmation email to property owner upon registration
- Notify admin of new pending registrations
- Send approval notification to property owner

### 2. Enhanced Validation
- Add password strength requirements
- Implement email verification
- Add CAPTCHA to prevent spam registrations

### 3. User Experience Improvements
- Add "Forgot Password" functionality
- Implement password reset flow
- Add account activation workflow

## Conclusion

The property owner registration feature provides a secure, controlled way for property owners to request access to the system while ensuring that only approved users can log in. The implementation follows security best practices and integrates seamlessly with the existing authentication system.