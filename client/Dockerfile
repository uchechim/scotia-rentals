#Frontend Dockerfile

#Python image to be used for container
FROM node:14

#Working Directory
WORKDIR /app

# Copy the package.json and package-lock.json for installation purposes
COPY package*.json ./

#install dependencies
RUN npm install

#Copy rest of application files into the container
COPY . .

#Build App for production
RUN npm run build

#Use NGINX container to serve React App
FROM nginx:alpine

#Copy the built files from the first stage to the 
#nginx server's root directory.
COPY --from=0 /app/build /usr/share/nginx/html

#Expose port 80 for HTTP traffic
EXPOSE 80

#Start NGINX server
CMD ["nginx", "-g", "daemon off;"]