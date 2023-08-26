package com.example.polemonweathermap.services;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.io.File;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Objects;
import java.util.stream.Collectors;

@Service
public class ForecastImageService {

    //public ResponseEntity<byte[]> getImage(String selectedDate){
    public File getImage(String selectedDate){
        ArrayList<String> data = new ArrayList<>(Arrays.asList(selectedDate.split("-")));

        // Ahora puedes acceder a los componentes de la fecha
        String year = data.get(0);
        String month = data.get(1);
        String day = data.get(2);


        String path = "images/spain/" + year + "/" + month + "/" + day;

        System.out.println("\n" + path);
        File directory = new File(path);
        if(directory.exists() && directory.isDirectory()){
            File[] fields = directory.listFiles();
            if (fields.length == 1){
                File image = fields[0];
                return image;
            }
        }
        System.out.println("mal directorio");
        return null;
    }
}
