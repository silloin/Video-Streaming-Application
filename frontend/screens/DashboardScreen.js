import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, TouchableOpacity, StyleSheet, ActivityIndicator, Button } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import API_URL from '../config';

export default function DashboardScreen({ navigation }) {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchVideos = async () => {
        try {
            const response = await axios.get(`${API_URL}/dashboard`);
            setVideos(response.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVideos();

        // Header Right: Settings Button
        navigation.setOptions({
            headerRight: () => (
                <Button title="Settings" onPress={() => navigation.navigate('Settings')} />
            ),
        });
    }, [navigation]);

    if (loading) return <ActivityIndicator style={{ flex: 1 }} />;

    return (
        <View style={styles.container}>
            <FlatList
                data={videos}
                keyExtractor={item => item.id}
                renderItem={({ item }) => (
                    <TouchableOpacity
                        style={styles.card}
                        onPress={() => navigation.navigate('VideoPlayer', { video: item })}
                    >
                        <Image source={{ uri: item.thumbnail_url }} style={styles.thumbnail} />
                        <View style={styles.info}>
                            <Text style={styles.title}>{item.title}</Text>
                            <Text style={styles.desc}>{item.description}</Text>
                        </View>
                    </TouchableOpacity>
                )}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5', padding: 10 },
    card: { backgroundColor: '#fff', borderRadius: 10, marginBottom: 15, overflow: 'hidden', elevation: 2 },
    thumbnail: { width: '100%', height: 200 },
    info: { padding: 15 },
    title: { fontSize: 18, fontWeight: 'bold', marginBottom: 5 },
    desc: { color: '#666' }
});
