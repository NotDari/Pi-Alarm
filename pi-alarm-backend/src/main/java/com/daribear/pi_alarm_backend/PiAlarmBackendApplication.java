package com.daribear.pi_alarm_backend;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.CommandLineRunner;

@SpringBootApplication
public class PiAlarmBackendApplication implements CommandLineRunner{


	public static void main(String[] args) {
		SpringApplication.run(PiAlarmBackendApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

	}

}
