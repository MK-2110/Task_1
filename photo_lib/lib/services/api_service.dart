import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:photo_lib/models/photo.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.1.5:8000/api'; // Replace with your backend URL

  static Future<List<Photo>> getPhotos() async {
    final response = await http.get(Uri.parse('http://192.168.1.5:8000/api/photos'));
    if (response.statusCode == 200) {
      final List<dynamic> photoList = jsonDecode(response.body);
      return photoList.map((json) => Photo.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load photos: ${response.statusCode}');
    }
  }

  static Future<dynamic> uploadPhoto(String filePath) async {
    var request = http.MultipartRequest('POST', Uri.parse('http://192.168.1.5:8000/api/photos/upload'));
    request.files.add(await http.MultipartFile.fromPath('image', filePath));
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to upload photo: ${response.statusCode} - ${response.body}');
    }
  }
}