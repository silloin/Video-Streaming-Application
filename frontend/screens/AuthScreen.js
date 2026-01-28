import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import API_URL from '../config';

export default function AuthScreen({ navigation }) {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');

    const submit = async () => {
        const endpoint = isLogin ? '/auth/login' : '/auth/signup';
        const payload = isLogin ? { email, password } : { name, email, password };

        try {
            const response = await axios.post(`${API_URL}${endpoint}`, payload);
            const { token } = response.data;
            await AsyncStorage.setItem('token', token);
            navigation.replace('Dashboard');
        } catch (error) {
            Alert.alert('Error', error.response?.data?.error || 'Something went wrong');
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>{isLogin ? 'Login' : 'Signup'}</Text>

            {!isLogin && (
                <TextInput
                    placeholder="Name"
                    style={styles.input}
                    value={name}
                    onChangeText={setName}
                />
            )}
            <TextInput
                placeholder="Email"
                style={styles.input}
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
            />
            <TextInput
                placeholder="Password"
                style={styles.input}
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />

            <Button title={isLogin ? "Login" : "Sign Up"} onPress={submit} />

            <TouchableOpacity onPress={() => setIsLogin(!isLogin)} style={styles.switch}>
                <Text style={styles.switchText}>
                    {isLogin ? "Need an account? Sign Up" : "Have an account? Login"}
                </Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: '#fff' },
    header: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
    input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 15, borderRadius: 5 },
    switch: { marginTop: 20, alignItems: 'center' },
    switchText: { color: 'blue' }
});
