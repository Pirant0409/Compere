/**
 * This is an automatically generated file
 * @name Hello world
 * @kind problem
 * @problem.severity warning
 * @id java/example/hello-world
 */

 import java


 from Method method
 where method.getLocation().getFile().getBaseName() = "GameController.java" and
         method.getName() = "moveRight"
 select method.getBody().getLocation(), "method"