$(document).ready(function () {
    console.log("jquery is running")
    $("#getRecommendationBtn").click(function (e) {
        e.preventDefault();
        console.log("Get Recommendation button clicked")

        // Get values from form
        let formData = new FormData($("#cropRecommendationForm")[0]);

        // Clear previous validation errors 
        $("#nitrogen_error").text(""); 
        $("#phosphorus_error").text(""); 
        $("#potassium_error").text(""); 
        $("#temperature_error").text(""); 
        $("#humidity_error").text(""); 
        $("#ph_error").text(""); 
        $("#rainfall_error").text("");

        // AJAX request
        $.ajax({
            url: "/crop/predict/",
            type: "POST",
            data: formData,
            processData: false, 
            contentType: false,

            // When Django returns response
            success: function (response) {
                console.log(response);

                if (response.status) {
                    $("#crop-name").text(response.prediction);
                    $("#crop-image").attr("src",response.image_url);
                    $("#result-card").show();
                }
                else { 
                    // Display field validation errors 
                    if (response.errors){ 
                        if (response.errors.nitrogen){ 
                            $("#nitrogen_error") .text(response.errors.nitrogen[0]); 
                        } 
                        if (response.errors.phrosphorus){
                            $("#phosphorus_error") .text(response.errors.phrosphorus[0]); 
                        } 
                        if (response.errors.potassium){
                            $("#potassium_error") .text(response.errors.potassium[0]); 
                        } 
                        if (response.errors.temperature){
                            $("#temperature_error") .text(response.errors.temperature[0]); 
                        } 
                        if (response.errors.humidity){ 
                            $("#humidity_error") .text(response.errors.humidity[0]); 
                        } 
                        if (response.errors.ph){ 
                            $("#ph_error") .text(response.errors.ph[0]); 
                        }
                        if (response.errors.rainfall){ 
                            $("#rainfall_error") .text(response.errors.rainfall[0]); 
                        } 
                    }
                }
            },
            // If error occurs

            error: function (error) {
                console.log(error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // yield Prediction
    $("#yieldPredictionBtn").click(function(e) {
        e.preventDefault();
        console.log("Get prediction for yield button clicked")

        let formData = new FormData($("#yieldPredictionForm")[0]);

        $.ajax({
            url: "/yield/prediction-yield/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,

            success: function(response) {
                // Clear previous errors
                    $("#crop_type_error").text("");
                    $("#soil_type_error").text("");
                    $("#temperature_error").text("");
                    $("#humidity_error").text("");
                    $("#rainfall_error").text("");
                    $("#season_error").text("");

                if (response.status) {
                    $("#yield-value").text(response.crop_yield + " tons/hectare");
                    $("#yield-result").show();
                }

                else {
                    // Display field validation errors
                    if (response.errors) {

                        if (response.errors.crop_type) {
                            $("#crop_type_error").text(response.errors.crop_type[0]);
                        }

                        if (response.errors.soil_type) {
                            $("#soil_type_error").text(response.errors.soil_type[0]);
                        }

                        if (response.errors.temperature) {
                            $("#temperature_error").text(response.errors.temperature[0]);
                        }

                        if (response.errors.humidity) {
                            $("#humidity_error").text(response.errors.humidity[0]);
                        }

                        if (response.errors.rainfall) {
                            $("#rainfall_error").text(response.errors.rainfall[0]);
                        }

                        if (response.errors.season) {
                            $("#season_error").text(response.errors.season[0]);
                        }
                    }
                } 
            },
            
            error: function (error) {
                console.log(error);
                alert("Something went wrong. Please try again.");
            }
        });
    });
});

// -----------------------------------------------------------------------------


// Plant Disease Prediction
$("#diseasePredictionBtn").click(function(e) {
    e.preventDefault();
    console.log("Disease prediction started");

    let formData = new FormData($("#uploadForm")[0]);

    $.ajax({
        url: "/disease/predict/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,

        success: function(response) {
            console.log(response);

            if (response.status) {
                // Show uploaded image
                $("#uploadedDiseaseImage").attr("src", response.image_url)
                $("#uploadedImageSection").show();

                // Show result card
                $("#resultSection").show();

                // Initially pending
                $("#predictionStatus").text("⏳ Pending...");
                $("#diseaseResult").text("");

                // Start checking status
                checkDiseaseStatus(response.prediction_id);
            }
        },

        error: function(error) {
            console.log(error);
            alert("Something went wrong. Please try again.");
        }
    });
});

// status pooling
function checkDiseaseStatus(predictionId){
    $.ajax({
        url: "/disease/status/" + predictionId + "/",
        type: "GET",

        success: function(response) {
            console.log("Prediction status:", response.status);

            if (response.status === "PENDING") {
                $("#predictionStatus").text("⏳ Pending...");

                setTimeout(function() {
                    checkDiseaseStatus(predictionId);
                }, 3000);
            }

            else if (response.status === "PROCESSING") {
                $("#predictionStatus").text("🔄 Processing...");

                setTimeout(function() {
                    checkDiseaseStatus(predictionId);
                }, 3000);

            }

            else if (response.status === "COMPLETED") {
                $("#predictionStatus").text("✓ Completed");
                $("#diseaseResult").text(response.disease_name);
            }

            else if (response.status === "FAILED") {
                $("#predictionStatus").text("❌ Prediction Failed");
            }
        },

        error: function(error) {
            console.log(error);
        }
    });
}

