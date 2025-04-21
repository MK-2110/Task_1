class Photo {
  final String filename;
  final int? id;

  Photo({required this.filename, this.id});

  factory Photo.fromJson(Map<String, dynamic> json) {
    return Photo(
      filename: json['filename'] as String,
      id: json['id'] as int?,
    );
  }
}