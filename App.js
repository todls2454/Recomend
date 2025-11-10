// App.js
import React, { useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  StyleSheet,
} from "react-native";

export default function App() {
  const [userId, setUserId] = useState("user1");
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // 이 주소는 너 서버 주소로 바꿔
  const API_URL = "http://10.0.2.2:8000/recommend"; 
  // 안드로이드 에뮬레이터: 10.0.2.2
  // iOS 시뮬레이터: http://localhost:8000

  const fetchRecs = async () => {
    setLoading(true);
    setErrorMsg("");
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, k: 5 }),
      });
      const data = await res.json();
      setRecs(data.recommendations || []);
    } catch (err) {
      setErrorMsg("추천을 불러오지 못했어.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>추천 시스템 테스트</Text>

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={userId}
          onChangeText={setUserId}
          placeholder="user id 입력"
          autoCapitalize="none"
        />
        <Button title="추천받기" onPress={fetchRecs} />
      </View>

      {loading && <Text>불러오는 중...</Text>}
      {errorMsg ? <Text style={styles.error}>{errorMsg}</Text> : null}

      <FlatList
        data={recs}
        keyExtractor={(item, idx) => item + idx}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>{item}</Text>
          </View>
        )}
        ListEmptyComponent={
          !loading ? <Text>추천 결과가 없습니다.</Text> : null
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: "#fff" },
  title: { fontSize: 20, fontWeight: "600", marginBottom: 16 },
  inputRow: { flexDirection: "row", gap: 8, alignItems: "center" },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 4,
    paddingHorizontal: 8,
    height: 40,
  },
  item: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  error: { color: "red", marginTop: 8 },
});