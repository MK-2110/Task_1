import 'package:flutter/material.dart';
import 'package:photo_lib/screens/photo_list_screen.dart';

void main() {
  runApp(const PhotoLibraryApp());
}

class PhotoLibraryApp extends StatelessWidget {
  const PhotoLibraryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Photo Library',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const PhotoListScreen(),
    );
  }
}