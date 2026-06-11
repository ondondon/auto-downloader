import 'dart:io';
import 'package:flutter/material.dart';

void main() {
  runApp(const AutoDownloaderApp());
}

class AutoDownloaderApp extends StatelessWidget {
  const AutoDownloaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Auto-Downloader',
      theme: ThemeData.dark(),
      home: const DownloadPage(),
    );
  }
}

class DownloadPage extends StatefulWidget {
  const DownloadPage({super.key});

  @override
  State<DownloadPage> createState() => _DownloadPageState();
}

class _DownloadPageState extends State<DownloadPage> {
  final _urlController = TextEditingController();
  final _logController = TextEditingController();
  bool _isDownloading = false;

  String _detectPlatform(String url) {
    if (url.contains('twitter.com') || url.contains('x.com')) return 'Twitter/X';
    if (url.contains('pixiv.net')) return 'Pixiv';
    if (url.contains('instagram.com')) return 'Instagram';
    if (url.contains('reddit.com')) return 'Reddit';
    if (url.contains('danbooru')) return 'Danbooru';
    return 'Auto-detect';
  }

  Future<void> _download() async {
    final url = _urlController.text.trim();
    if (url.isEmpty) return;

    setState(() {
      _isDownloading = true;
      _logController.text = 'Starting download...\n';
      _logController.text += 'URL: $url\n';
      _logController.text += 'Platform: ${_detectPlatform(url)}\n';
      _logController.text += 'Output: /storage/emulated/0/Download/AutoDownloader\n\n';
    });

    try {
      final result = await Process.run(
        'gallery-dl',
        ['--no-check-certificate', '-D', '/storage/emulated/0/Download/AutoDownloader', url],
      );

      setState(() {
        if (result.exitCode == 0) {
          _logController.text += '✅ Download completed!\n';
          _logController.text += result.stdout.toString().substring(0, 500);
        } else {
          _logController.text += '❌ Download failed!\n';
          _logController.text += result.stderr.toString().substring(0, 500);
        }
        _isDownloading = false;
      });
    } catch (e) {
      setState(() {
        _logController.text += '❌ Error: $e\n';
        _isDownloading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Auto-Downloader'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Gallery Downloader',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _urlController,
              decoration: InputDecoration(
                labelText: 'URL',
                hintText: 'https://twitter.com/...',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () => _urlController.clear(),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Platform: ${_detectPlatform(_urlController.text)}',
              style: TextStyle(color: Colors.grey[400]),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _isDownloading ? null : _download,
              icon: const Icon(Icons.download),
              label: Text(_isDownloading ? 'Downloading...' : 'Download'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
              ),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey[700]!),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _logController.text.isEmpty ? 'Logs will appear here...' : _logController.text,
                    style: const TextStyle(fontFamily: 'monospace', fontSize: 12),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}