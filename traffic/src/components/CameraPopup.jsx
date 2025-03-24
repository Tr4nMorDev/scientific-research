import { motion } from "framer-motion";

const CameraPopup = ({ camera, onClose }) => {
  return (
    <motion.div
      className="fixed inset-0 bg-opacity-50 flex items-center justify-center z-20 backdrop-blur-sm"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <motion.div
        className="bg-white p-6 rounded-xl shadow-lg w-2/3"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        exit={{ scale: 0.8 }}
        transition={{ duration: 0.3 }}
      >
        <h2 className="text-2xl font-bold mb-4">{camera.name}</h2>
        <p className="text-lg">{camera.description}</p>
        {camera.videoUrl ? (
          <video
            src={camera.videoUrl}
            controls
            autoPlay
            className="w-full mt-4 rounded-lg"
          />
        ) : (
          <p>Không tìm thấy video</p>
        )}
        <button
          onClick={onClose}
          className="mt-4 bg-red-500 text-white px-4 py-2 rounded-lg"
        >
          Đóng
        </button>
      </motion.div>
    </motion.div>
  );
};

export default CameraPopup;
