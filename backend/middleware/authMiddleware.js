const jwt = require("jsonwebtoken");

const authMiddleware = (req, res, next) => {
  const token = req.header("Authorization")?.replace("Bearer ", "");

  if (!token) {
    return res.status(401).json({ message: "ไม่มี Token การเข้าถึงถูกปฏิเสธ" });
  }

  try {
    const decoded = jwt.verify(token, "SECRET_KEY");
    req.user_id = decoded.user_id; // เพิ่มข้อมูลผู้ใช้งานใน request object
    next();
  } catch (error) {
    res.status(401).json({ message: "Token ไม่ถูกต้อง" });
  }
};

module.exports = authMiddleware;