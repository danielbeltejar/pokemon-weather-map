package com.example.polemonweathermap.controllers;

import com.example.polemonweathermap.services.ForecastImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.File;
import java.io.IOException;
import java.net.http.HttpHeaders;
import java.nio.file.Files;
import java.nio.file.Path;

@Controller
public class principalController {

    @Autowired
    private ForecastImageService forecastImageService;

    @GetMapping
    public String show(){
        return "index";
    }


    @PostMapping("/forecast")
    public ResponseEntity<byte[]> handleForecast(@RequestParam("datePicker") String dateString) {
        File image = forecastImageService.getImage(dateString);
        if (image == null){
            return ResponseEntity.notFound().build();
        }
        else {
            try {
                byte[] imageBytes = Files.readAllBytes(Path.of(image.getPath()));

                return ResponseEntity.ok().contentType(MediaType.IMAGE_JPEG).body(imageBytes);
            } catch (IOException e) {
                e.printStackTrace();
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            }
        }
    }



}
