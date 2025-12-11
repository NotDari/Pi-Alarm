package com.daribear.pi_alarm_backend.Errors;

import jakarta.servlet.http.HttpServletResponse;

public class ErrorStorage {

    public enum ErrorType{

        UserDetailsIncorrect(HttpServletResponse.SC_UNAUTHORIZED,1 , "Invalid Username/Password"),
        UserAccountLocked(HttpServletResponse.SC_UNAUTHORIZED,2,  "Account is locked"),
        UserAccountDisabled(HttpServletResponse.SC_UNAUTHORIZED,3,  "Account is disabled"),
        InternalError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR,4,  "Internal Server Error"),
        UnknownError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR,5,  "Unknown Error"),
        UserLoggedOut(HttpServletResponse.SC_UNAUTHORIZED,6,  "User logged out"),
        NOAUTHATTEMPTED(HttpServletResponse.SC_UNAUTHORIZED,7,  "No Auth attempted"),

        REGEMAILTAKE(HttpServletResponse.SC_UNAUTHORIZED,8,  "Registration Email Taken"),

        USERNOTFOUND(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, 9, "User not found"),

        REGISTEREMAILNOTVALID(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, 10, "Email not valid");
        public final Integer responseCode;
        public final Integer errorCode;
        public final String message;



        ErrorType(Integer responseCode,Integer errorCode, String message) {
            this.responseCode = responseCode;
            this.errorCode = errorCode;
            this.message = message;
        }
    }

    public static CustomError getCustomErrorFromType(ErrorType errorType){
        return new CustomError(errorType.responseCode, errorType.message, errorType.errorCode);
    }

}