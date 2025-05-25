-- Create places table if it doesn't exist
CREATE TABLE IF NOT EXISTS places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert all places
INSERT INTO places (name, latitude, longitude, timezone) VALUES
-- Andhra Pradesh
('Anantapur', 14.6819, 77.6006, 'Asia/Kolkata'),
('Chittoor', 13.2156, 79.1004, 'Asia/Kolkata'),
('East Godavari', 17.0, 82.0, 'Asia/Kolkata'),
('Guntur', 16.3008, 80.4428, 'Asia/Kolkata'),
('Krishna', 16.1667, 81.1333, 'Asia/Kolkata'),
('Kurnool', 15.8281, 78.0373, 'Asia/Kolkata'),
('Nellore', 14.4426, 79.9865, 'Asia/Kolkata'),
('Prakasam', 15.5, 80.0, 'Asia/Kolkata'),
('Srikakulam', 18.3, 83.9, 'Asia/Kolkata'),
('Visakhapatnam', 17.6868, 83.2185, 'Asia/Kolkata'),
('Vizianagaram', 18.1167, 83.4167, 'Asia/Kolkata'),
('West Godavari', 16.7, 81.1, 'Asia/Kolkata'),
('YSR Kadapa', 14.4667, 78.8167, 'Asia/Kolkata'),

-- Tamil Nadu
('Ariyalur', 11.1333, 79.0833, 'Asia/Kolkata'),
('Chennai', 13.0827, 80.2707, 'Asia/Kolkata'),
('Coimbatore', 11.0168, 76.9558, 'Asia/Kolkata'),
('Cuddalore', 11.75, 79.75, 'Asia/Kolkata'),
('Dharmapuri', 12.1277, 78.1579, 'Asia/Kolkata'),
('Dindigul', 10.35, 77.95, 'Asia/Kolkata'),
('Erode', 11.3428, 77.7274, 'Asia/Kolkata'),
('Kancheepuram', 12.8397, 79.7006, 'Asia/Kolkata'),
('Karur', 10.95, 78.0833, 'Asia/Kolkata'),
('Krishnagiri', 12.5204, 78.2139, 'Asia/Kolkata'),
('Madurai', 9.9252, 78.1198, 'Asia/Kolkata'),
('Nagapattinam', 10.7667, 79.8333, 'Asia/Kolkata'),
('Namakkal', 11.2167, 78.1667, 'Asia/Kolkata'),
('Perambalur', 11.2333, 78.8833, 'Asia/Kolkata'),
('Pudukkottai', 10.3833, 78.8167, 'Asia/Kolkata'),
('Ramanathapuram', 9.3833, 78.8333, 'Asia/Kolkata'),
('Salem', 11.65, 78.1667, 'Asia/Kolkata'),
('Sivaganga', 9.8667, 78.4833, 'Asia/Kolkata'),
('Thanjavur', 10.8, 79.15, 'Asia/Kolkata'),
('Theni', 10.0167, 77.4833, 'Asia/Kolkata'),
('Thoothukudi', 8.7833, 78.1333, 'Asia/Kolkata'),
('Tiruchirappalli', 10.8050, 78.6856, 'Asia/Kolkata'),
('Tirunelveli', 8.7289, 77.7081, 'Asia/Kolkata'),
('Tiruppur', 11.1075, 77.3398, 'Asia/Kolkata'),
('Tiruvallur', 13.1333, 79.9167, 'Asia/Kolkata'),
('Tiruvannamalai', 12.2269, 79.0745, 'Asia/Kolkata'),
('Tiruvarur', 10.7725, 79.6368, 'Asia/Kolkata'),
('Vellore', 12.9167, 79.1333, 'Asia/Kolkata'),
('Viluppuram', 11.9333, 79.4833, 'Asia/Kolkata'),
('Virudhunagar', 9.5833, 77.95, 'Asia/Kolkata'),

-- Kerala
('Alappuzha', 9.5, 76.5, 'Asia/Kolkata'),
('Ernakulam', 9.98, 76.28, 'Asia/Kolkata'),
('Idukki', 9.85, 76.97, 'Asia/Kolkata'),
('Kannur', 11.87, 75.37, 'Asia/Kolkata'),
('Kasaragod', 12.5, 75.0, 'Asia/Kolkata'),
('Kollam', 8.88, 76.6, 'Asia/Kolkata'),
('Kottayam', 9.58, 76.52, 'Asia/Kolkata'),
('Kozhikode', 11.25, 75.77, 'Asia/Kolkata'),
('Malappuram', 11.07, 76.07, 'Asia/Kolkata'),
('Palakkad', 10.78, 76.65, 'Asia/Kolkata'),
('Pathanamthitta', 9.27, 76.78, 'Asia/Kolkata'),
('Thiruvananthapuram', 8.48, 76.95, 'Asia/Kolkata'),
('Thrissur', 10.52, 76.21, 'Asia/Kolkata'),
('Wayanad', 11.6, 76.08, 'Asia/Kolkata'),

-- Karnataka
('Bagalkot', 16.18, 75.7, 'Asia/Kolkata'),
('Ballari', 15.15, 76.93, 'Asia/Kolkata'),
('Belagavi', 15.87, 74.5, 'Asia/Kolkata'),
('Bengaluru Rural', 12.97, 77.59, 'Asia/Kolkata'),
('Bengaluru Urban', 12.97, 77.59, 'Asia/Kolkata'),
('Bidar', 17.92, 77.52, 'Asia/Kolkata'),
('Chamarajanagar', 11.92, 76.95, 'Asia/Kolkata'),
('Chikballapur', 13.43, 77.72, 'Asia/Kolkata'),
('Chikkamagaluru', 13.32, 75.77, 'Asia/Kolkata'),
('Chitradurga', 14.23, 76.4, 'Asia/Kolkata'),
('Dakshina Kannada', 12.87, 74.88, 'Asia/Kolkata'),
('Davanagere', 14.47, 75.92, 'Asia/Kolkata'),
('Dharwad', 15.37, 75.02, 'Asia/Kolkata'),
('Gadag', 15.42, 75.62, 'Asia/Kolkata'),
('Hassan', 13.0, 76.1, 'Asia/Kolkata'),
('Haveri', 14.8, 75.4, 'Asia/Kolkata'),
('Kalaburagi', 17.33, 76.83, 'Asia/Kolkata'),
('Kodagu', 12.42, 75.73, 'Asia/Kolkata'),
('Kolar', 13.13, 78.13, 'Asia/Kolkata'),
('Koppal', 15.35, 76.15, 'Asia/Kolkata'),
('Mandya', 12.52, 76.9, 'Asia/Kolkata'),
('Mysuru', 12.3, 76.65, 'Asia/Kolkata'),
('Raichur', 16.2, 77.37, 'Asia/Kolkata'),
('Ramanagara', 12.72, 77.28, 'Asia/Kolkata'),
('Shivamogga', 13.93, 75.57, 'Asia/Kolkata'),
('Tumakuru', 13.33, 77.1, 'Asia/Kolkata'),
('Udupi', 13.33, 74.75, 'Asia/Kolkata'),
('Uttara Kannada', 14.68, 74.48, 'Asia/Kolkata'),
('Vijayapura', 16.82, 75.72, 'Asia/Kolkata'),
('Yadgir', 16.77, 77.13, 'Asia/Kolkata'),

-- Maharashtra
('Mumbai', 19.0760, 72.8777, 'Asia/Kolkata'),
('Pune', 18.5204, 73.8567, 'Asia/Kolkata'),
('Nagpur', 21.1458, 79.0882, 'Asia/Kolkata'),
('Thane', 19.2183, 72.9781, 'Asia/Kolkata'),
('Pimpri-Chinchwad', 18.6279, 73.8009, 'Asia/Kolkata'),
('Nashik', 20.0059, 73.7897, 'Asia/Kolkata'),
('Kalyan-Dombivli', 19.2350, 73.1299, 'Asia/Kolkata'),
('Vasai-Virar', 19.4259, 72.8225, 'Asia/Kolkata'),
('Aurangabad', 19.8762, 75.3433, 'Asia/Kolkata'),
('Navi Mumbai', 19.0330, 73.0297, 'Asia/Kolkata'),

-- Delhi NCR
('New Delhi', 28.6139, 77.2090, 'Asia/Kolkata'),
('Gurgaon', 28.4595, 77.0266, 'Asia/Kolkata'),
('Noida', 28.5355, 77.3910, 'Asia/Kolkata'),
('Faridabad', 28.4089, 77.3178, 'Asia/Kolkata'),
('Ghaziabad', 28.6692, 77.4538, 'Asia/Kolkata'),

-- West Bengal
('Kolkata', 22.5726, 88.3639, 'Asia/Kolkata'),
('Asansol', 23.6739, 86.9524, 'Asia/Kolkata'),
('Siliguri', 26.7271, 88.3953, 'Asia/Kolkata'),
('Durgapur', 23.5204, 87.3119, 'Asia/Kolkata'),
('Bardhaman', 23.2400, 87.8700, 'Asia/Kolkata'),

-- Gujarat
('Ahmedabad', 23.0225, 72.5714, 'Asia/Kolkata'),
('Surat', 21.1702, 72.8311, 'Asia/Kolkata'),
('Vadodara', 22.3072, 73.1812, 'Asia/Kolkata'),
('Rajkot', 22.3039, 70.8022, 'Asia/Kolkata'),
('Bhavnagar', 21.7645, 72.1519, 'Asia/Kolkata'),

-- Rajasthan
('Jaipur', 26.9124, 75.7873, 'Asia/Kolkata'),
('Jodhpur', 26.2389, 73.0243, 'Asia/Kolkata'),
('Kota', 25.2138, 75.8648, 'Asia/Kolkata'),
('Bikaner', 28.0229, 73.3119, 'Asia/Kolkata'),
('Ajmer', 26.4499, 74.6399, 'Asia/Kolkata'),

-- Uttar Pradesh
('Lucknow', 26.8467, 80.9462, 'Asia/Kolkata'),
('Kanpur', 26.4499, 80.3319, 'Asia/Kolkata'),
('Agra', 27.1767, 78.0081, 'Asia/Kolkata'),
('Varanasi', 25.3176, 82.9739, 'Asia/Kolkata'),
('Allahabad', 25.4358, 81.8463, 'Asia/Kolkata'),

-- Punjab
('Ludhiana', 30.9010, 75.8573, 'Asia/Kolkata'),
('Amritsar', 31.6340, 74.8723, 'Asia/Kolkata'),
('Jalandhar', 31.3260, 75.5762, 'Asia/Kolkata'),
('Patiala', 30.3398, 76.3869, 'Asia/Kolkata'),
('Bathinda', 30.2070, 74.9455, 'Asia/Kolkata'),

-- Haryana
('Panipat', 29.3909, 76.9635, 'Asia/Kolkata'),
('Ambala', 30.3782, 76.7767, 'Asia/Kolkata'),
('Yamunanagar', 30.1290, 77.2674, 'Asia/Kolkata'),

-- Madhya Pradesh
('Indore', 22.7196, 75.8577, 'Asia/Kolkata'),
('Bhopal', 23.2599, 77.4126, 'Asia/Kolkata'),
('Jabalpur', 23.1815, 79.9864, 'Asia/Kolkata'),
('Gwalior', 26.2183, 78.1828, 'Asia/Kolkata'),
('Ujjain', 23.1765, 75.7885, 'Asia/Kolkata'),

-- Bihar
('Patna', 25.5941, 85.1376, 'Asia/Kolkata'),
('Gaya', 24.7955, 85.0000, 'Asia/Kolkata'),
('Bhagalpur', 25.2445, 86.9718, 'Asia/Kolkata'),
('Muzaffarpur', 26.1209, 85.3647, 'Asia/Kolkata'),
('Darbhanga', 26.1522, 85.8970, 'Asia/Kolkata'),

-- Odisha
('Bhubaneswar', 20.2961, 85.8245, 'Asia/Kolkata'),
('Cuttack', 20.4625, 85.8830, 'Asia/Kolkata'),
('Rourkela', 22.2604, 84.8536, 'Asia/Kolkata'),
('Berhampur', 19.3149, 84.7941, 'Asia/Kolkata'),
('Sambalpur', 21.4704, 83.9701, 'Asia/Kolkata'),

-- Telangana
('Hyderabad', 17.3850, 78.4867, 'Asia/Kolkata'),
('Warangal', 17.9689, 79.5941, 'Asia/Kolkata'),
('Nizamabad', 18.6725, 78.0941, 'Asia/Kolkata'),
('Karimnagar', 18.4386, 79.1288, 'Asia/Kolkata'),
('Ramagundam', 18.8000, 79.4500, 'Asia/Kolkata'),

-- Assam
('Guwahati', 26.1445, 91.7362, 'Asia/Kolkata'),
('Silchar', 24.8333, 92.7789, 'Asia/Kolkata'),
('Dibrugarh', 27.4728, 94.9120, 'Asia/Kolkata'),
('Jorhat', 26.7509, 94.2037, 'Asia/Kolkata'),
('Nagaon', 26.3509, 92.6925, 'Asia/Kolkata'),

-- Jharkhand
('Ranchi', 23.3441, 85.3096, 'Asia/Kolkata'),
('Jamshedpur', 22.8046, 86.2029, 'Asia/Kolkata'),
('Dhanbad', 23.7957, 86.4304, 'Asia/Kolkata'),
('Bokaro Steel City', 23.6693, 86.1511, 'Asia/Kolkata'),
('Hazaribagh', 24.0000, 85.3500, 'Asia/Kolkata'),

-- Chhattisgarh
('Raipur', 21.2514, 81.6296, 'Asia/Kolkata'),
('Bhilai', 21.2092, 81.4285, 'Asia/Kolkata'),
('Bilaspur', 22.0735, 82.1398, 'Asia/Kolkata'),
('Korba', 22.3458, 82.6963, 'Asia/Kolkata'),
('Durg', 21.1900, 81.2800, 'Asia/Kolkata'),

-- Uttarakhand
('Dehradun', 30.3165, 78.0322, 'Asia/Kolkata'),
('Haridwar', 29.9457, 78.1642, 'Asia/Kolkata'),
('Roorkee', 29.8543, 77.8880, 'Asia/Kolkata'),
('Haldwani', 29.2183, 79.5191, 'Asia/Kolkata'),
('Rudrapur', 28.9800, 79.4000, 'Asia/Kolkata'),

-- Himachal Pradesh
('Shimla', 31.1048, 77.1734, 'Asia/Kolkata'),
('Solan', 30.9045, 77.0967, 'Asia/Kolkata'),
('Dharamshala', 32.2190, 76.3234, 'Asia/Kolkata'),
('Mandi', 31.7084, 76.9314, 'Asia/Kolkata'),
('Bilaspur', 31.3383, 76.7564, 'Asia/Kolkata'),

-- Jammu and Kashmir
('Srinagar', 34.0837, 74.7973, 'Asia/Kolkata'),
('Jammu', 32.7266, 74.8570, 'Asia/Kolkata'),
('Anantnag', 33.7311, 75.1547, 'Asia/Kolkata'),
('Baramulla', 34.2095, 74.3428, 'Asia/Kolkata'),
('Udhampur', 32.9167, 75.1333, 'Asia/Kolkata'),

-- Goa
('Panaji', 15.4909, 73.8278, 'Asia/Kolkata'),
('Vasco da Gama', 15.3860, 73.8158, 'Asia/Kolkata'),
('Margao', 15.2735, 73.9573, 'Asia/Kolkata'),
('Mapusa', 15.5915, 73.8089, 'Asia/Kolkata'),
('Ponda', 15.4036, 74.0152, 'Asia/Kolkata'),

-- Manipur
('Imphal', 24.8170, 93.9368, 'Asia/Kolkata'),
('Thoubal', 24.6380, 94.0100, 'Asia/Kolkata'),
('Bishnupur', 24.6333, 93.7667, 'Asia/Kolkata'),
('Churachandpur', 24.3333, 93.6833, 'Asia/Kolkata'),
('Ukhrul', 25.1167, 94.3667, 'Asia/Kolkata'),

-- Meghalaya
('Shillong', 25.5788, 91.8933, 'Asia/Kolkata'),
('Tura', 25.5167, 90.2167, 'Asia/Kolkata'),
('Jowai', 25.4500, 92.2000, 'Asia/Kolkata'),
('Nongpoh', 25.9000, 91.8833, 'Asia/Kolkata'),
('Williamnagar', 25.5000, 90.6167, 'Asia/Kolkata'),

-- Nagaland
('Kohima', 25.6667, 94.1167, 'Asia/Kolkata'),
('Dimapur', 25.9000, 93.7333, 'Asia/Kolkata'),
('Mokokchung', 26.3333, 94.5333, 'Asia/Kolkata'),
('Tuensang', 26.2833, 94.8333, 'Asia/Kolkata'),
('Wokha', 26.1000, 94.2667, 'Asia/Kolkata'),

-- Tripura
('Agartala', 23.8315, 91.2868, 'Asia/Kolkata'),
('Udaipur', 23.5333, 91.4833, 'Asia/Kolkata'),
('Dharmanagar', 24.3667, 92.1667, 'Asia/Kolkata'),
('Kailashahar', 24.3333, 92.0167, 'Asia/Kolkata'),
('Belonia', 23.2500, 91.4500, 'Asia/Kolkata'),

-- Mizoram
('Aizawl', 23.7271, 92.7176, 'Asia/Kolkata'),
('Lunglei', 22.8833, 92.7333, 'Asia/Kolkata'),
('Saiha', 22.4833, 92.9667, 'Asia/Kolkata'),
('Champhai', 23.4667, 93.3167, 'Asia/Kolkata'),
('Kolasib', 24.2333, 92.6833, 'Asia/Kolkata'),

-- Arunachal Pradesh
('Itanagar', 27.1000, 93.6167, 'Asia/Kolkata'),
('Naharlagun', 27.1000, 93.7000, 'Asia/Kolkata'),
('Tawang', 27.5833, 91.8667, 'Asia/Kolkata'),
('Bomdila', 27.2667, 92.4000, 'Asia/Kolkata'),
('Pasighat', 28.0667, 95.3333, 'Asia/Kolkata'),

-- Sikkim
('Gangtok', 27.3389, 88.6065, 'Asia/Kolkata'),
('Namchi', 27.1667, 88.3500, 'Asia/Kolkata'),
('Mangan', 27.5167, 88.5333, 'Asia/Kolkata'),
('Gyalshing', 27.2833, 88.2667, 'Asia/Kolkata'),
('Singtam', 27.2333, 88.5000, 'Asia/Kolkata'),

-- Andaman and Nicobar Islands
('Port Blair', 11.6667, 92.7500, 'Asia/Kolkata'),
('Diglipur', 13.2667, 92.9833, 'Asia/Kolkata'),
('Mayabunder', 12.9333, 92.9333, 'Asia/Kolkata'),
('Rangat', 12.5000, 92.9167, 'Asia/Kolkata'),
('Hut Bay', 10.6000, 92.5333, 'Asia/Kolkata'),

-- Lakshadweep
('Kavaratti', 10.5626, 72.6369, 'Asia/Kolkata'),
('Agatti', 10.8500, 72.2000, 'Asia/Kolkata'),
('Amini', 11.1167, 72.7333, 'Asia/Kolkata'),
('Andrott', 10.8333, 73.6667, 'Asia/Kolkata'),
('Kadmat', 11.2333, 72.7833, 'Asia/Kolkata'),

-- Puducherry
('Puducherry', 11.9416, 79.8083, 'Asia/Kolkata'),
('Karaikal', 10.9167, 79.8333, 'Asia/Kolkata'),
('Mahe', 11.7000, 75.5333, 'Asia/Kolkata'),
('Yanam', 16.7333, 82.2167, 'Asia/Kolkata'),

-- Chandigarh
('Chandigarh', 30.7333, 76.7794, 'Asia/Kolkata'),

-- Dadra and Nagar Haveli and Daman and Diu
('Daman', 20.4167, 72.8500, 'Asia/Kolkata'),
('Diu', 20.7167, 70.9833, 'Asia/Kolkata'),
('Silvassa', 20.2667, 73.0167, 'Asia/Kolkata'),

-- World Cities
-- North America
('New York', 40.7128, -74.0060, 'America/New_York'),
('Los Angeles', 34.0522, -118.2437, 'America/Los_Angeles'),
('Chicago', 41.8781, -87.6298, 'America/Chicago'),
('Toronto', 43.6532, -79.3832, 'America/Toronto'),
('Vancouver', 49.2827, -123.1207, 'America/Vancouver'),
('Mexico City', 19.4326, -99.1332, 'America/Mexico_City'),

-- South America
('São Paulo', -23.5505, -46.6333, 'America/Sao_Paulo'),
('Rio de Janeiro', -22.9068, -43.1729, 'America/Sao_Paulo'),
('Buenos Aires', -34.6037, -58.3816, 'America/Argentina/Buenos_Aires'),
('Lima', -12.0464, -77.0428, 'America/Lima'),
('Bogotá', 4.7110, -74.0721, 'America/Bogota'),

-- Europe
('London', 51.5074, -0.1278, 'Europe/London'),
('Paris', 48.8566, 2.3522, 'Europe/Paris'),
('Berlin', 52.5200, 13.4050, 'Europe/Berlin'),
('Rome', 41.9028, 12.4964, 'Europe/Rome'),
('Madrid', 40.4168, -3.7038, 'Europe/Madrid'),
('Moscow', 55.7558, 37.6173, 'Europe/Moscow'),

-- Asia
('Tokyo', 35.6762, 139.6503, 'Asia/Tokyo'),
('Beijing', 39.9042, 116.4074, 'Asia/Shanghai'),
('Shanghai', 31.2304, 121.4737, 'Asia/Shanghai'),
('Hong Kong', 22.3193, 114.1694, 'Asia/Hong_Kong'),
('Singapore', 1.3521, 103.8198, 'Asia/Singapore'),
('Seoul', 37.5665, 126.9780, 'Asia/Seoul'),
('Dubai', 25.2048, 55.2708, 'Asia/Dubai'),

-- Australia and Oceania
('Sydney', -33.8688, 151.2093, 'Australia/Sydney'),
('Melbourne', -37.8136, 144.9631, 'Australia/Melbourne'),
('Auckland', -36.8485, 174.7633, 'Pacific/Auckland'),
('Honolulu', 21.3069, -157.8583, 'Pacific/Honolulu'),

-- Africa
('Cairo', 30.0444, 31.2357, 'Africa/Cairo'),
('Johannesburg', -26.2041, 28.0473, 'Africa/Johannesburg'),
('Nairobi', -1.2921, 36.8219, 'Africa/Nairobi'),
('Lagos', 6.5244, 3.3792, 'Africa/Lagos'),
('Cape Town', -33.9249, 18.4241, 'Africa/Johannesburg'); 