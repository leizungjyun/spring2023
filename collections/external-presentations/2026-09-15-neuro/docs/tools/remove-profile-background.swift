import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins
import ImageIO
import Darwin
import ObjectiveC

let context = CIContext(options: [.useSoftwareRenderer: false])
let directory = URL(fileURLWithPath: CommandLine.arguments[1])
for (name, ext) in [("朱祥维", "png"), ("王腾", "jpeg"), ("李颂元", "jpeg")] {
    let input = directory.appendingPathComponent(name + "." + ext)
    guard let source = CIImage(contentsOf: input) else { fatalError("Cannot load portrait") }
    // Runtime lookup supports Macs whose installed SDK predates this Vision API.
    guard let requestClass = NSClassFromString("VNGeneratePersonSegmentationRequest") else { fatalError("Person segmentation unavailable") }
    typealias Create = @convention(c) (AnyClass, Selector) -> AnyObject
    let create = unsafeBitCast(dlsym(dlopen(nil, RTLD_NOW), "objc_msgSend"), to: Create.self)
    let request = create(requestClass, NSSelectorFromString("new")) as! VNRequest
    request.setValue(0, forKey: "qualityLevel") // accurate
    request.setValue(kCVPixelFormatType_OneComponent8, forKey: "outputPixelFormat")
    try VNImageRequestHandler(url: input, options: [:]).perform([request])
    guard let result = request.results?.first as? VNPixelBufferObservation else { fatalError("No person mask") }
    let mask = CIImage(cvPixelBuffer: result.pixelBuffer)
    let scaledMask = mask.transformed(by: CGAffineTransform(scaleX: source.extent.width / mask.extent.width, y: source.extent.height / mask.extent.height))
    let blend = CIFilter.blendWithMask()
    blend.inputImage = source
    blend.backgroundImage = CIImage(color: .clear).cropped(to: source.extent)
    blend.maskImage = scaledMask
    guard let output = blend.outputImage else { fatalError("Cannot compose cutout") }
    try context.writePNGRepresentation(of: output, to: directory.appendingPathComponent(name + "-transparent.png"), format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
    print("Saved transparent portrait: \(name)")
}
