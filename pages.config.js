export default {
  build: {
    command: "yarn install --network-timeout 300000 && yarn build",
    directory: "build",
  },
  rootDirectory: "frontend",
};
