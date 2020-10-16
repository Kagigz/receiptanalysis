import * as React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { TabView, SceneMap } from 'react-native-tab-view';
import TopBar from './TopBar'
import ImagePick from './ImagePick';

const ReceiptsRoute = () => (
  <ImagePick/>
);

const OverviewRoute = () => (
  <View style={[styles.scene, { backgroundColor: '#673ab7' }]} />
);

const initialLayout = { width: Dimensions.get('window').width, height: 0.8*Dimensions.get('window').height };

export default function TabViewExample() {
  const [index, setIndex] = React.useState(0);
  const [routes] = React.useState([
    { key: 'receipts', title: 'Receipts' },
    { key: 'overview', title: 'Overview' },
  ]);

  const renderScene = SceneMap({
    receipts: ReceiptsRoute,
    overview: OverviewRoute,
  });

  return (
        <TabView
        navigationState={{ index, routes }}
        renderScene={renderScene}
        onIndexChange={setIndex}
        initialLayout={initialLayout}
        />
  );
}

const styles = StyleSheet.create({
  scene: {
    flex: 1,
  }
});