import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, Alert, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import API_URL from '../config';

export default function VideoPlayerScreen({ route }) {
    const { video } = route.params;
    const [streamUrl, setStreamUrl] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStream = async () => {
            try {
                const token = await AsyncStorage.getItem('token');
                if (!token) return;

                const response = await axios.get(`${API_URL}/video/${video.id}/stream`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                setStreamUrl(response.data.stream_url);
            } catch (error) {
                Alert.alert('Error', 'Failed to load video stream');
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchStream();
    }, [video]);

    if (loading) return <ActivityIndicator style={styles.center} />;

    if (!streamUrl) return <View style={styles.center}><ActivityIndicator /></View>;

    return (
        <WebView
            source={{ uri: streamUrl }}
            style={{ flex: 1, backgroundColor: 'black' }}
            allowsFullscreenVideo
            javaScriptEnabled
            domStorageEnabled
        />
    );
}

const styles = StyleSheet.create({
    center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' }
});
