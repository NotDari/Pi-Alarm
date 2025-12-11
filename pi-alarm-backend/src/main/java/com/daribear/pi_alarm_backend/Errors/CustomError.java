package com.daribear.pi_alarm_backend.Errors;

import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
public class CustomError extends RuntimeException {
    private Integer httpStatus;
    private String message;
    private Integer customCode;

    public CustomError(Integer httpsServletResponse, String message, Integer customCode) {
        this.httpStatus = httpsServletResponse;
        this.message = message;
        this.customCode = customCode;
    }

}
